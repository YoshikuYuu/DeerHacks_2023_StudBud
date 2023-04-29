def check_in_db(ctx):
    # checking if they're already in db
    username = ctx.author.name
    discriminator = ctx.author.discriminator
    user_id = f"{username}#{discriminator}"
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()

    # if they're not in db add them
    if not result:
        username = ctx.author.name
        discriminator = ctx.author.discriminator
        user_id = f"{username}#{discriminator}"
        cursor.execute("INSERT INTO users (user_id, task) VALUES (?, '')", (user_id,))
        conn.commit()
    else:
        await ctx.send('You have already registered!')
