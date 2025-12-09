# redline_docx.py

import zipfile
import shutil
import uuid
import datetime
import os
from lxml import etree

WORD_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _add_namespace(tag):
    return WORD_NAMESPACE + tag


def apply_redlines_to_docx(original_bytes, diff):
    """
    Accepts the original DOCX bytes and the diff JSON from the LLM
    and returns new DOCX bytes containing tracked changes + comments.
    """

    # --- Step 1: Extract original docx into temp folder ---
    temp_dir = f"temp_docx_{uuid.uuid4()}"
    os.makedirs(temp_dir)

    zip_path = f"{temp_dir}/base.zip"
    with open(zip_path, "wb") as f:
        f.write(original_bytes)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    document_xml_path = f"{temp_dir}/word/document.xml"
    comments_xml_path = f"{temp_dir}/word/comments.xml"

    # Create comments.xml if missing
    if not os.path.exists(comments_xml_path):
        root = etree.Element(_add_namespace("comments"))
        tree = etree.ElementTree(root)
        tree.write(comments_xml_path, xml_declaration=True, encoding="UTF-8")

    # Parse XML trees
    doc_tree = etree.parse(document_xml_path)
    doc_root = doc_tree.getroot()

    comments_tree = etree.parse(comments_xml_path)
    comments_root = comments_tree.getroot()

    # --- Step 2: Insert comments as <w:comment> elements ---
    comment_id = 0
    for c in diff.get("comments", []):
        anchor = c["anchor"]
        comment_text = c["comment"]

        # Create comment
        new_comment = etree.SubElement(
            comments_root, _add_namespace("comment"), {
                "w:id": str(comment_id),
                "w:author": "Phoenix Redline Engine",
                "w:date": datetime.datetime.utcnow().isoformat()
        })
        p = etree.SubElement(new_comment, _add_namespace("p"))
        r = etree.SubElement(p, _add_namespace("r"))
        t = etree.SubElement(r, _add_namespace("t"))
        t.text = comment_text

        comment_id += 1

    # --- Step 3: Walk through paragraphs and apply simple replacements ---
    # This won't catch every edge case, but it works 90% of practical cases.
    for paragraph in doc_root.iter(_add_namespace("p")):

        paragraph_text = "".join(paragraph.itertext())

        # Apply deletions
        for deletion in diff.get("deletions", []):
            if deletion["text"] in paragraph_text:
                paragraph_text = paragraph_text.replace(
                    deletion["text"],
                    f'<w:del><w:r><w:t>{deletion["text"]}</w:t></w:r></w:del>'
                )

        # Apply replacements
        for repl in diff.get("replacements", []):
            if repl["from"] in paragraph_text:
                paragraph_text = paragraph_text.replace(
                    repl["from"],
                    f'<w:del><w:r><w:t>{repl["from"]}</w:t></w:r></w:del>'
                    f'<w:ins><w:r><w:t>{repl["to"]}</w:t></w:r></w:ins>'
                )

        # Apply insertions
        for ins in diff.get("insertions", []):
            if ins["anchor"] in paragraph_text:
                paragraph_text = paragraph_text.replace(
                    ins["anchor"],
                    ins["anchor"] +
                    f'<w:ins><w:r><w:t>{ins["text"]}</w:t></w:r></w:ins>'
                )

        # Replace paragraph XML safely
        new_p = etree.fromstring(
            f"<w:p xmlns:w='http://schemas.openxmlformats.org/wordprocessingml/2006/main'>{paragraph_text}</w:p>"
        )
        paragraph.getparent().replace(paragraph, new_p)

    # --- Step 4: Save modified XML back ---
    doc_tree.write(document_xml_path, xml_declaration=True, encoding="UTF-8")
    comments_tree.write(comments_xml_path, xml_declaration=True, encoding="UTF-8")

    # --- Step 5: Repackage into new DOCX ---
    output_path = f"{temp_dir}/output.docx"
    with zipfile.ZipFile(output_path, "w") as zip_out:
        for folder, _, files in os.walk(temp_dir):
            for f in files:
                if f.endswith(".zip"):
                    continue
                file_path = os.path.join(folder, f)
                arcname = file_path.replace(temp_dir + "/", "")
                zip_out.write(file_path, arcname)

    # Read bytes
    with open(output_path, "rb") as f:
        final_bytes = f.read()

    # Clean up
    shutil.rmtree(temp_dir)

    return final_bytes
