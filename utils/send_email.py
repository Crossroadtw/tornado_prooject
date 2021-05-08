from email.mime.text import MIMEText
import smtplib

from email.utils import parseaddr, formataddr
from email.header import Header

from config import SETTING


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def sned_email(content, email=SETTING.MY_EMAIL):
    # 发邮件
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr('来自 <%s>' % SETTING.EMAIL_ADMIN)
    msg['To'] = _format_addr('管理员 <%s>' % email)
    msg['Subject'] = Header('来自Chione', 'utf-8').encode()
    server = smtplib.SMTP_SSL(SETTING.SMTP_SERVER, 465)
    server.set_debuglevel(1)
    server.login(SETTING.EMAIL_ADMIN, SETTING.EMAIL_PASSWORD)
    server.sendmail(SETTING.EMAIL_ADMIN, [email], msg.as_string())
    server.quit()


if __name__ == '__main__':
    sned_email('测试', 'xxx@qq.com')
