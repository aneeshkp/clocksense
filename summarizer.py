def generate_daily_summary(chunks):
    out = []
    for i, c in enumerate(chunks, 1):
        first = c.splitlines()[0] if c else ''
        out.append(f"Chunk {i}: {len(c.splitlines())} lines. First: {first}")
    return "\n".join(out)
