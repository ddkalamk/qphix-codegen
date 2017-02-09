#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2017 Martin Ueding <dev@martin-ueding.de>

import argparse
import json
import os

import jinja2


def main():
    with open('isa.js') as f:
        isas = json.load(f)

    kernels = [
        ('clov_dslash', 'clov_%(fptype)s_dslash'),
        ('dslash', 'dslash'),
        ('tmf_dslash', 'tmf_dslash'),
        ('tmf_clov_dslash', 'tmf_clov_%(fptype)s_dslash'),
    ]

    # Setting up Jinja
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('..')
    )
    complete_specialization = env.get_template('jinja/complete_specialization.j2.h')

    for isa, isa_data in isas.items():
        if not os.path.isdir(os.path.join('..', isa)):
            print('Code for ISA `{}` is not generated. Skipping.'.format(isa))
            continue

        for kernel, kernel_pattern in kernels:
            print('Working on kernel `{}` for ISA `{}` …'.format(kernel, isa))
            defines = [
                (fptype, fptype_data['veclen'], fptype_data['soalens'])
                for fptype, fptype_data in isa_data['fptypes'].items()]

            rendered = complete_specialization.render(
                ISA=isa,
                kernel_base=kernel,
                kernel_pattern=kernel_pattern,
                defines=defines,
            )

            os.makedirs(isa, exist_ok=True)
            filename = os.path.join(isa, '{}_{}_complete_specialization.h'.format(kernel, isa))
            with open(filename, 'w') as f:
                f.write(rendered)


def _parse_args():
    '''
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    '''
    parser = argparse.ArgumentParser(description='')
    options = parser.parse_args()

    return options


if __name__ == "__main__":
    main()
