# -*- coding: utf-8 -*-


def identifier(i):
    return i.replace('ä', 'a').replace('ö', 'o').replace(' ', '_').lower()
