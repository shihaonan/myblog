import click
import app

def register_commands(app):
    @app.cli.command()
    @click.option('--category',default =10,help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category,post,comment):
        """Generates the fake categories, posts, and comments."""
        from app.fakes import fake_admin,fake_bloginfo,fake_categories,fake_posts,fake_comments

        click.echo('生成管理员。。。')
        fake_admin()
        click.echo('生成博客信息。。。')
        fake_bloginfo()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)
        click.echo('Generating %d posts...' % post)
        fake_posts(post)
        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Done.')















