def writein(title, subtitle):
    with open(f"{title}.md", "w") as f:
        f.write(subtitle)