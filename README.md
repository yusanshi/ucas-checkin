# 国科大每日健康打卡

中国科学院大学每日健康打卡脚本 Headless Browsers 版，中科大学生请勿使用。

## 背景

国科大每日健康打卡系统的字段经常变动，采用手动 POST 的思路时可能需要频繁更改代码，而采用 headless browsers 模拟前端操作的思路，当字段发生变化时，手动打卡一次即可，无需更改代码。

## 免责声明

1. 仅用于中国科学院大学每日健康打卡，其他高校（如中科大）学生请勿使用；
2. 本脚本仅用于辅助使用者减少重复工作量（如连续多天信息没有变动时避免每天需手动打卡），使用者需对本脚本所做的所有操作负责。当使用者的健康打卡信息发生变动时应主动及时在健康打卡系统中手动更新信息。

## 开始

- 环境要求：

    - 一个 24 小时开机的 Linux 操作系统（需要使用 systemd，如 Ubuntu 16.04, Debian Jessie, CentOS 7, Fedora 等，树莓派也行）
    - Python 3.6+
      - 如果 `/usr/bin/python3 --version` 命令显示的 Python 3 版本号低于 3.6，请额外安装 Python 3.6 或以上版本，并将本 README 和 `ucas-checkin.service` 中出现的 `/usr/bin/python3` 全部换成 `/usr/bin/python3.X`，如您安装了 Python 3.8，则将 `/usr/bin/python3` 换成 `/usr/bin/python3.8`
      - Python 3.6+ 的要求是为了安装 torch 用于验证码的识别（为什么只要不是校园网就一直有验证码？）

-   ```bash
    git clone https://github.com/yusanshi/ucas-checkin && cd ucas-checkin
    sudo /usr/bin/python3 -m pip install selenium easyocr
    sudo apt-get install chromium-chromedriver # 非 Ubuntu/Debian 系统自行使用合适的包管理器安装
    sudo cp ucas-checkin.py /root/ucas-checkin.py
    sudo cp ucas-checkin.{service,timer} /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable --now ucas-checkin.timer
    ```

- 在 `/root` 目录下创建 [`ucas-checkin.txt` 文件](ucas-checkin.example.txt)，填入以下内容：

    ```ini
    USERNAME=你的CAS登录学号
    PASSWORD=你的CAS登录密码
    ```

你可以使用 `sudo -i /usr/bin/python3 /root/ucas-checkin.py` 命令来测试打卡。首次运行需要下载用于 OCR 的模型文件，请耐心等待。如您的下载速度过慢或无法下载，请使用以下命令手动下载：
```bash
wget https://storage.yusanshi.com/easyocr.tar.gz
sudo rm -rfv /root/.EasyOCR
sudo tar -xzvf easyocr.tar.gz -C /root
rm easyocr.tar.gz
```
为什么只要不是校园网就一直有验证码？


本脚本默认在每天 8:00 至 11:00 之间随机选择一个时间打卡一次，请确保你的系统时钟和时区设置是正确的，或者自行编辑 `ucas-checkin.timer` 文件设置打卡时间。

你可以使用 `systemctl status ucas-checkin.timer` 查看打卡记录和下次打卡时间。

如您希望打卡失败时自动通知自己，请在 `ucas-checkin.py` 文件中的 `notify_myself` 函数中加入通知的代码（推荐使用邮件、Telegram 机器人等方式）。您也可以省略此操作，因为绑定了国科大企业微信之后，如当天没有打卡，会自动在 12:00 左右收到提醒信息（这也是为什么本脚本设置的最后打卡时间在 11:00 :)


## 致谢

systemd 的配置文件和本 README 中的`开始`部分借鉴于 [iBug/thu-checkin](https://github.com/iBug/thu-checkin) 项目。

