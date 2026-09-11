#!/usr/bin/env python3
"""Measure content overflow per page."""
import os
from playwright.sync_api import sync_playwright

PAGES = ['06','07','08','09','10']

with sync_playwright() as p:
    browser = p.chromium.launch()
    for num in PAGES:
        src = f'/home/z/my-project/downloads/instagram-DcaW1UljsVk/recreated-page-{num}.html'
        page = browser.new_page(viewport={'width':1300,'height':1900})
        page.goto('file://'+src)
        page.wait_for_load_state('networkidle')
        info = page.evaluate('''() => {
            const content = document.querySelector('.content');
            const paper = content.parentElement;
            const pr = paper.getBoundingClientRect();
            const last = content.lastElementChild;
            const lr = last ? last.getBoundingClientRect() : null;
            return {
                paper_h: pr.height,
                content_scroll_h: content.scrollHeight,
                content_client_h: content.clientHeight,
                last_bottom: lr ? lr.bottom : null,
                last_class: last ? last.className : null,
            };
        }''')
        overflow = info['content_scroll_h'] - info['content_client_h']
        last_bottom_rel = info['last_bottom'] - 48 if info['last_bottom'] else 0
        print(f'page-{num}: paper_h={info["paper_h"]:.0f} '
              f'content_scroll={info["content_scroll_h"]:.0f} '
              f'client={info["content_client_h"]:.0f} '
              f'overflow={overflow:.0f}px '
              f'last_bottom_rel={last_bottom_rel:.0f} '
              f'last_class="{info["last_class"]}"')
        page.close()
    browser.close()
