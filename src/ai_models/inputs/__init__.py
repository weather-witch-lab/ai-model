# (C) Copyright 2023 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import logging
from functools import cached_property

import earthkit.data as ekd
import earthkit.regrid as ekr
import entrypoints
from earthkit.data.indexing.fieldlist import FieldArray

LOG = logging.getLogger(__name__)


def get_input(name, *args, **kwargs):
    return available_inputs()[name].load()(*args, **kwargs)


def available_inputs():
    result = {}
    for e in entrypoints.get_group_all("ai_models.input"):
        result[e.name] = e
    return result
