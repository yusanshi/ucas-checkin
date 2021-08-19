# 国科大每日健康打卡

中国科学院大学每日健康打卡脚本 Headless Browsers 版，中科大学生请勿使用。

## 背景

国科大每日健康打卡系统的字段经常变动，采用手动 POST 的思路时可能需要频繁更改代码，而采用 headless browsers 模拟前端操作的思路，当字段发生变化时，手动打卡一次即可，无需更改代码。

## 免责声明

1. 仅用于中国科学院大学每日健康打卡，其他高校（如中科大）学生请勿使用；
2. 本脚本仅用于辅助使用者减少重复工作量（如连续多天信息没有变动时避免每天需手动打卡），使用者需对本脚本所做的所有操作负责。当使用者的健康打卡信息发生变动时应主动及时在健康打卡系统中手动更新信息。

## 开始

- 环境要求：一个 24 小时开机的 Linux 操作系统（需要使用 systemd，如 Ubuntu 16.04, Debian Jessie, CentOS 7, Fedora 等，树莓派也行），Python 3.5+；

-   ```bash
    git clone https://github.com/yusanshi/ucas-checkin && cd ucas-checkin
    sudo pip3 install -r requirements.txt
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

本脚本默认在每天 8:00 至 11:00 之间随机选择一个时间打卡一次，请确保你的系统时钟和时区设置是正确的，或者自行编辑 `ucas-checkin.timer` 文件设置打卡时间。

你可以使用 `systemctl status ucas-checkin.timer` 查看打卡记录和下次打卡时间。

如您希望打卡失败时自动通知自己，请在 `ucas-checkin.py` 文件中的 `notify_myself` 函数中加入通知的代码（推荐使用邮件、Telegram 机器人等方式）。您也可以省略此操作，因为绑定了国科大企业微信之后，如当天没有打卡，会自动在 12:00 左右收到提醒信息（这也是为什么本脚本设置的最后打卡时间在 11:00 :)


## 致谢

systemd 的配置文件和本 README 中的`开始`部分借鉴于 [iBug/thu-checkin](https://github.com/iBug/thu-checkin) 项目。

