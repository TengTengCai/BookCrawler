from datetime import datetime


class ErrorLog(object):
    def __init__(self):
        self._file_name = 'Error.log'

    def write_error(self, error_str):
        try:
            with open(self._file_name, 'a', encoding='utf-8') as f:
                now = datetime.now()
                error_str = now + ': ' + error_str
                f.write(error_str)
        except Exception as e:
            print('错误日志写入失败！', e)

    def clear_error_log(self):
        try:
            with open(self._file_name, 'w', encoding='utf-8') as f:
                f.write('\n')
        except Exception as e:
            print('错误日志清空失败！', e)
