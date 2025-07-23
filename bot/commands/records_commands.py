'''

emoji_results = []

        for png in new_pngs:
            emoji_name = sanitize_emoji_name(png)
            file_path = os.path.join(ASSET_DIR, png)

            with open(file_path, "rb") as image:
                try:
                    emoji = await guild.create_custom_emoji(name=emoji_name, image=image.read())
                    emoji_results.append(f"Created emoji `:{emoji.name}:` <:{emoji.name}:{emoji.id}>")
                except discord.HTTPException as e:
                    emoji_results.append(f"Failed to upload `{emoji_name}`: {e}")

        summary = "\n".join(emoji_results)
        summary += f"\n\nSuccessfully converted **{converted}** SVG(s) and uploaded them as custom emojis."

        await interaction.followup.send(summary, ephemeral=False)

'''