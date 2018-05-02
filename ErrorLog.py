from datetime import datetime


class ErrorLog(object):
    """错误日志记录类"""
    def __init__(self):
        """错误日志类"""
        self._file_name = 'Error.log'  # 初始化日志文件名

    def write_error(self, error_str):
        """
        错误写入

        :param error_str: 错误消息
        :return: None
        """
        try:
            # 打开文件
            with open(self._file_name, 'a', encoding='utf-8') as f:
                now = datetime.now()  # 获取时间
                error_str = str(now) + ': ' + str(error_str)  # 错误信息拼接时间
                f.write(error_str)  # 写入数据
        except Exception as e:
            print('错误日志写入失败！', e)  # 写入错误日志

    def clear_error_log(self):
        """
        没有文件就创建，有就清空文件

        :return: None
        """
        try:
            # 打开文件
            with open(self._file_name, 'w', encoding='utf-8') as f:
                f.write('\n')  # 写入内容
        except Exception as e:
            print('错误日志清空失败！', e)  # 写入错误日志
