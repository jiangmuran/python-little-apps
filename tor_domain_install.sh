#!/bin/bash

echo "====================="
echo "  Tor 安装、启动、配置向导"
echo "====================="

PS3='请选择一个操作：'
options=("安装 Tor" "启动 Tor" "停止 Tor" "重启 Tor" "查看 Tor 状态" "修改 Tor 配置" "添加转发" "查看当前转发" "删除转发" "查看域名" "退出")
select opt in "${options[@]}"
do
    case $opt in
        "安装 Tor")
            # 安装 Tor
            echo
            echo "正在安装 Tor..."
            sudo apt-get update
            sudo apt-get install tor -y
            echo "Tor 安装完成。"
            ;;
        "启动 Tor")
            # 启动 Tor
            echo
            echo "正在启动 Tor..."
            sudo service tor start
            echo "Tor 启动完成。"
            ;;
        "停止 Tor")
            # 停止 Tor
            echo
            echo "正在停止 Tor..."
            sudo service tor stop
            echo "Tor 已停止。"
            ;;
        "重启 Tor")
            # 重启 Tor
            echo
            echo "正在重启 Tor..."
            sudo service tor restart
            echo "Tor 重启完成。"
            ;;
        "查看 Tor 状态")
            # 查看 Tor 状态
            echo
            echo "正在查看 Tor 状态..."
            sudo service tor status
            ;;
        "修改 Tor 配置")
            # 配置向导
            echo
            echo "现在，请按照提示配置 Tor。"

            # 询问 SOCKSPort 参数
            echo
            echo "请设置 SOCKSPort 参数，按回车键使用默认值 9050："
            read socksport
            if [ -z "$socksport" ]; then
                socksport=9050
            fi

            # 询问 Log 参数
            echo
            echo "请设置 Log 参数，按回车键使用默认值 notice file /var/log/tor/notices.log："
            read log
            if [ -z "$log" ]; then
                log="notice file /var/log/tor/notices.log"
            fi

            # 询问 DataDirectory 参数
            echo
            echo "请设置 DataDirectory 参数，按回车键使用默认值 /var/lib/tor："
            read datadir
            if [ -z "$datadir" ]; then
                datadir="/var/lib/tor"
            fi

            # 询问 HiddenServiceDir 参数
            echo
            echo "请设置 HiddenServiceDir 参数，按回车键使用默认值 /var/lib/tor/hidden_service/："
            read hiddenservicedir
            if [ -z "$hiddenservicedir" ]; then
                hiddenservicedir="/var/lib/tor/hidden_service/"
            fi

            # 询问 HiddenServicePort 参数
            echo
            echo "请设置 HiddenServicePort 参数，按回车键使用默认值 80 127.0.0.1:80："
            read hiddenport
            if [ -z "$hiddenport" ]; then
                hiddenport="80 127.0.0.1:80"
            fi
        # 将参数写入配置文件
        sudo sed -i "s/SOCKSPort.*/SOCKSPort $socksport/g" /etc/tor/torrc
        sudo sed -i "s/#Log.*/$log/g" /etc/tor/torrc
        sudo sed -i "s/DataDirectory.*/DataDirectory $datadir/g" /etc/tor/torrc
        sudo sed -i "s/#HiddenServiceDir.*/HiddenServiceDir $hiddenservicedir/g" /etc/tor/torrc
        sudo sed -i "s/#HiddenServicePort.*/HiddenServicePort $hiddenport/g" /etc/tor/torrc

        # 重启 Tor
        sudo service tor restart
        echo "Tor 配置已更新。"
        ;;
    "添加转发")
        # 添加转发
        echo
        echo "现在，请按照提示添加转发。"

        # 询问源地址
        echo
        echo "请输入源地址（例如：127.0.0.1:8080）："
        read source_addr

        # 询问目标地址
        echo
        echo "请输入目标地址（例如：example.onion:80）："
        read target_addr

        # 将转发写入配置文件
        echo "mapaddress $source_addr $target_addr" | sudo tee -a /etc/tor/torrc

        # 重启 Tor
        sudo service tor restart
        echo "转发已添加。"
        ;;
    "查看当前转发")
        # 查看当前转发
        echo
        echo "正在查看当前转发..."
        sudo grep -E "^mapaddress.*$" /etc/tor/torrc
        ;;
    "删除转发")
        # 删除转发
        echo
        echo "现在，请按照提示删除转发。"

        # 询问源地址
        echo
        echo "请输入要删除的源地址（例如：127.0.0.1:8080）："
        read source_addr

        # 将转发从配置文件中删除
        sudo sed -i "/^mapaddress $source_addr/d" /etc/tor/torrc

        # 重启 Tor
        sudo service tor restart
        echo "转发已删除。"
        ;;
    "查看域名")
        # 查看域名
        echo
        echo "现在，请按照提示查看域名。"

        # 询问隐藏服务目录
        echo
        echo "请输入隐藏服务目录（例如：/var/lib/tor/hidden_service/）："
        read hiddenservicedir

        # 读取 hostname 文件
        cat "$hiddenservicedir/hostname"
        ;;
    "退出")
        break
        ;;
    *) echo "无效的操作 $REPLY";;
esac
