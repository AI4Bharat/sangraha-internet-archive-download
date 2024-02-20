from internetarchive import get_item, search_items
import os

def get_identifiers_for_language(language, language_code):
    """
    Get unique identifiers from internet archive which consists of PDFs

    Input: language, language code
    returns: identifiers
    """
    identifiers = []
    query = 'language:({} OR {}) AND mediatype:(texts) AND format:(PDF)'.format(language, language_code)
    search_results = search_items(query,sorts=['downloads desc'])
    count = 0
    for i in search_results:
        count += 1
        identifiers.append(i['identifier'])
    return identifiers

def dowload_identifier_data(identifier,language,destination_folder,pdf_only=True):
    """
    Download Identifier associated files

    Input: identifier,language,destination folder,pdf_only
    returns: identifiers
    """
    item = get_item(identifier)
    try: 
        destnation_path = f"{destination_folder}/{language}/{identifier}/"
        if not os.path.exists(destnation_path):
            os.makedirs(destnation_path)
        if pdf_only:
            item.download(glob_pattern='*.pdf', destdir=destnation_path,exclude_pattern="*_text.pdf", no_directory=True, ignore_errors=True, ignore_existing=True)
        else:
            item.download(destdir=destnation_path,no_directory=True, ignore_errors=True, ignore_existing=True)
    except:
        return False
    return True

def getItemMetaData(identifier):
    """
    Fetch Identifier Metadata

    Input: identifier
    returns: metadata list for identifier
    """
    item = get_item(identifier=identifier)
    files = item.get_files()
    pdfDataSize = 0
    totalDataSize = 0
    for file in files:
        if file.format=="Text PDF":
            pdfDataSize+=float(file.size)
        totalDataSize+=float(file.size)
    metadata = item.metadata
    subject = metadata.get("subject", "")
    ppi = metadata.get("ppi", "")
    title = metadata.get("title", "")
    ocr = metadata.get("ocr", "")
    description = metadata.get("description", "")
    date = metadata.get("publicdate", "")
    ialanguage = metadata.get("language", "")
    uploader = metadata.get("uploader", "")
    mediatype = metadata.get("mediatype", "")
    fields = [
        identifier,
        title,
        ppi,
        subject,
        ocr,
        description,
        date,
        ialanguage,
        uploader,
        mediatype,
    ]
    fields = [str(field) for field in fields]
    fields.append(totalDataSize)
    fields.append(pdfDataSize)
    return fields