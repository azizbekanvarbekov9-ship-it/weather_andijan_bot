deploy:
	@echo "Deploying the bot..."
	sudo systemctl stop sleep_mode2_bot.service
	sudo cp sleep_mode2_bot.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl start sleep_mode2_bot.service
	sudo systemctl enable sleep_mode2_bot.service
	@echo "Bot deployed successfully."

restart:
	@echo "Restarting the bot..."
	sudo systemctl restart sleep_mode2_bot.service

status:
	@echo "Checking the bot status..."
	sudo systemctl status sleep_mode2_bot.service
