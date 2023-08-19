from fetchers.sec_forms import get_latest_10K_url, get_form_text

if __name__ == '__main__':
    url = get_latest_10K_url(1318605)
    txt = get_form_text(url)
    with open('test.txt', 'w') as f:
        f.write('\n'.join(txt))
    