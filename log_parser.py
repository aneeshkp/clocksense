import re
from datetime import datetime

def parse_ptp_log(log_text):
    """
    Parses log text and returns:
      - parsed_data: list of dicts {timestamp, offset (ns), state}
      - time_chunks: list of text slices for summarization
    """
    iso_pattern = re.compile(r'(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)')
    offset_pattern = re.compile(r'offset[:=]?\s*([-+]?[0-9]*\.?[0-9]+)')
    state_pattern = re.compile(r'state is (\w+)')

    parsed = []
    lines = log_text.splitlines()
    for line in lines:
        iso = iso_pattern.search(line)
        if not iso:
            continue
        ts = datetime.fromisoformat(iso.group('ts').rstrip('Z'))
        off = offset_pattern.search(line)
        st = state_pattern.search(line)
        # Skip if neither
        if not (off or st):
            continue
        rec = {'timestamp': ts}
        if off:
            rec['offset'] = float(off.group(1))
        if st:
            rec['state'] = st.group(1)
        parsed.append(rec)

    # Chunk size based on lines (e.g., 100 lines per chunk)
    chunk_size = 100
    time_chunks = ["\n".join(lines[i:i+chunk_size]) for i in range(0, len(lines), chunk_size)]
    return parsed, time_chunks
