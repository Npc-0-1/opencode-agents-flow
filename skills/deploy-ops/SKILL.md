---
name: deploy-ops
description: "Use when working with Docker containers/images, service management (systemd/supervisor), deployment/service/server environment configuration, deployment verification, log inspection, health checks, or Linux server operations. Do not use for ordinary local dev environment config unless tied to deployment or service runtime. Triggers: deploy, docker, restart service, check logs, health check, deployment config, server ops."
---

# Deploy Operations

Manage Docker containers, services, and deployment verification. Focus on operation and verification, not infrastructure provisioning.

## Docker

Read-only inspection commands can run after confirming the target. Mutating/high-risk commands (`restart`, `up -d`, `down`, `build`, `push`, `exec` with writes) require explicit user authorization and a risk/recovery note.

```bash
# Containers
docker ps -a
docker logs --tail 100 <container>
docker restart <container>
docker exec -it <container> <command>
docker stats --no-stream
docker inspect <container>

# Images
docker images
docker build -t <name>:<tag> -f Dockerfile .
docker tag <name>:<tag> <registry>/<name>:<tag>
docker push <registry>/<name>:<tag>

# Compose
docker compose ps
docker compose logs --tail 50
docker compose up -d
docker compose down
docker compose restart <service>
docker compose exec <service> <command>
```

## Service Management

Status and log inspection are read-only. Restart/stop/start/reload commands require explicit user authorization and an interruption risk/recovery note.

```bash
# systemd
systemctl status <service>
systemctl restart <service>
journalctl -u <service> --since "10 min ago" -n 50

# supervisor
supervisorctl status
supervisorctl restart <service>
supervisorctl tail -100 <service>
```

## Deployment Verification

```bash
# Health check
curl -s -o /dev/null -w "%{http_code}" http://localhost:<port>/health
curl -s http://localhost:<port>/api/version

# Process check
ps aux | grep <process_name>
pgrep -a <process_name>

# Resource check
df -h
free -m
nvidia-smi  # if GPU
```

## Log Inspection

```bash
# Live tail
tail -f /var/log/<app>/app.log

# Error search
grep -i "error\|exception\|fatal" /var/log/<app>/app.log | tail -50

# Time range
sed -n '/2026-05-27 10:00/,/2026-05-27 11:00/p' /var/log/<app>/app.log
```

## Environment Config

- Check `.env` files exist and have required variables (report missing ones, do NOT write secrets).
- Verify config files syntax: `python -c "import json; json.load(open('config.json'))"` or similar.
- Check port bindings and file permissions.

## 二次确认（输出前必须执行）

- 反查命令参数是否正确，容器/服务名称是否准确。
- 确认操作影响范围：重启会中断什么，切换配置会影响什么。
- 非只读操作（restart/deploy/push）确认用户已授权。
