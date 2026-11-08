from pathlib import Path
import pymupdf


def read_pdf(file_path):
    file_path = Path(file_path)

    if not file_path.is_file():
        raise FileNotFoundError(f'Invalid file path: {file_path}')

    with pymupdf.open(file_path) as pdf:
        pages = [page.get_text() for page in pdf]

    text = '\n\n'.join(pages).strip()

    if not text:
        raise ValueError(f'No extractable text in {file_path.name} (scanned PDF?)')

    return text


if __name__ == '__main__':
    print(read_pdf(r'D:\BCS-3C-ke-bache\muhammadmustafa171-dld1.pdf')[:])