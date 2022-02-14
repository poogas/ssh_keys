#!/bin/bash

echo "Этот скрипт помогает быстро найти, кто имеет доступ к конкретному серверу."
echo "Введите имя сервера, который вас интересует:"
echo ""

read server_name

echo ""
echo "К серверу $server_name имеют доступ следующие сотрудники:"

find users -name "*.yml" -type f -exec grep -l "\- $server_name" {} \; | sed "s/users\///" | sed "s/.yml//"

echo ""
echo "Обратите внимание, что здесь не указаны те, кто имеет доступ ко всей этой группе серверов."
echo "Чтобы узнать у кого есть доступ к группе - выполните скрипт снова и на этот раз укажите имя группы."
echo ""