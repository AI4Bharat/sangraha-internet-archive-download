from archive_utils import get_identifiers_for_language,dowload_identifier_data,getItemMetaData
import os
import concurrent
import concurrent.futures
import pandas as pd
from tqdm import tqdm
import argparse

languages = [
    # top resource languages
    'English',
    'Assamese',
    'Bengali',
    'Gujarati',
    'Hindi',
    'Kannada',
    'Malayalam',
    'Marathi',
    'Oriya',
    'Punjabi',
    'Tamil',
    'Telugu',

    # bottom resource languages
    'Bodo',
    'Dogri',
    'Konkani', 
    'Kashmiri',
    'Maithili',
    'Manipuri',
    'Nepali',
    'Sanskrit',
    'Santali',
    'Sindhi',
    'Urdu',
]


languages_code = [
    # top resource codes
    'eng',
    'asm',
    'ben',
    'guj',
    'hin',
    'kan',
    'mal',
    'mar',
    'ori',
    'pan',
    'tam',
    'tel',

    # bottom resource codes
    'brx',
    'doi',
    'kok', 
    'kas',
    'mai',
    'mni',
    'nep',
    'san',
    'sat',
    'snd', 
    'urd',
]

language_dict = dict(zip(languages, languages_code))

def downloadIdentifiers(languages,languages_code,destdir):
    identifiers_list = []
    for language,language_code in list(zip(languages,languages_code)):
        print(f"Curating Identifiers for {language} ({language_code})")
        identifiers = get_identifiers_for_language(language=language,language_code=language_code)
        for identifier in identifiers:
            identifiers_list.append([identifier,language])

    identifierDataframe = pd.DataFrame(data=identifiers_list,columns=["identifier","language"])
    identifierDataframe.to_csv(f"{destdir}/identifiers.csv",index=False)
    print("Saved Identifiers to CSV Format")
    return f"{destdir}/identifiers.csv"

def downloadHelper(arguments):
    dowload_identifier_data(identifier=arguments[0],language=arguments[1],destination_folder=arguments[2],pdf_only=arguments[3])

parser = argparse.ArgumentParser()
parser.add_argument("--languages",action='store', dest='languageList',type=str, nargs='*',help="List of languages to download")
parser.add_argument("--pdf_only",type=bool,default=True,help="To download only associated PDF Files")
parser.add_argument("--id_only",type=bool,default=False,help="To download only identifiers file")

if __name__=="__main__":
    args = parser.parse_args()
    languagesToDownloadCodes = [language_dict[x] for x in args.languageList]
    data_path = "../../data/"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    if args.languageList:
        identifiersPath = downloadIdentifiers(args.languageList,languagesToDownloadCodes,data_path)
    else:
        identifiersPath = downloadIdentifiers(languages,languages_code,data_path)
    identifiersDf = pd.read_csv(identifiersPath)
    identifiersWithLanguage = []
    for idx,row in identifiersDf.iterrows():
        identifiersWithLanguage.append((row["identifier"],row["language"],data_path,True if args.pdf_only else False))

    metaExecutor = concurrent.futures.ProcessPoolExecutor()
    print("Fetching Metadata for Identifiers...")
    identifiers = [x[0] for x in identifiersWithLanguage]
    results = list(
        tqdm(metaExecutor.map(getItemMetaData, identifiers), total=len(identifiers))
    )

    resultDf = pd.DataFrame(
        data=results,
        columns=[
            "identifier",
            "title",
            "ppi",
            "subject",
            "ocr",
            "description",
            "date",
            "ialanguage",
            "uploader",
            "mediatype",
            "totalDataSize",
            "pdfDataSize"
        ],
    )

    resultDf.to_csv(f"{data_path}/identifiersMetaData.csv")
    print(f"Identifiers Metadata saved to {data_path}/identifiersMetaData.csv")
    metaExecutor.shutdown()

    if not args.id_only:
        downloadExecutor = concurrent.futures.ProcessPoolExecutor()
        print("Downloading Associated Files with Identifiers and Languages...")
        downloadSize = sum(resultDf["pdfDataSize"]) if args.pdf_only else sum(resultDf["totalDataSize"])
        print(f"Download Size : {downloadSize/(1024*1024)} MB")
        downloadResults = list(
            tqdm(downloadExecutor.map(downloadHelper, identifiersWithLanguage), total=len(identifiersWithLanguage))
        )
        downloadExecutor.shutdown()
        print("Files Downloaded from archive.org for associated Identifiers and Languages.")
    else:
        print("Download Complete")

