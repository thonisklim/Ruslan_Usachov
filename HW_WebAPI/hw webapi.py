from main.test_dropbox import TestDropBox
import main.config as cfg

if __name__ == '__main__':
    tester = TestDropBox(cfg.ACCESS_TOKEN, cfg.FILE_TO_UPLOAD, f'main/res/{cfg.FILE_TO_UPLOAD}')
    print(tester.file_upload())
    print(tester.file_get_metadata())
    print(tester.file_delete())
