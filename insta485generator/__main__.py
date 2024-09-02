"""Build static HTML site from directory of HTML templates and plain files."""
import click
import pathlib
import json
import jinja2
import shutil

@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Output directory.")
@click.option("-v", "--verbose", help="Print more output.")
def main(input_dir, output):
    """Templated static website generator"""

    input_dir = pathlib.Path(input_dir)
    config_filename = input_dir / 'config.json'
    template_dir = input_dir / "templates"

    with config_filename.open() as config_file:
        config_data = json.load(config_file)

    for page in config_data:
        url = pathlib.Path(page["url"].lstrip("/"))
        # template = template_dir / page["template"]
        output_dir = input_dir / "html" / url #default
        if output:
            output_dir = pathlib.Path(output)
        static_dir = input_dir/"static"
        if static_dir.is_dir():
            shutil.copytree(static_dir, output_dir, dirs_exist_ok=False)
        else:
            output_dir.mkdir(parents=True, exist_ok=True)

        template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(template_dir)),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
        )
        
        rendered_template = template_env.get_template(page["template"]).render(**page["context"])
        output_file = output_dir / "index.html"
        with open(output_file, 'w') as file:
            file.write(rendered_template)


if __name__ == "__main__":
    main()
