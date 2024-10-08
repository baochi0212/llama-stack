# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from typing import Optional

from llama_models.datatypes import ModelFamily

from llama_models.schema_utils import json_schema_type
from llama_models.sku_list import all_registered_models

from pydantic import BaseModel, Field, field_validator

from llama_toolchain.inference.api import QuantizationConfig


@json_schema_type
class MetaReferenceImplConfig(BaseModel):
    model: str = Field(
        default="Meta-Llama3.1-8B-Instruct",
        description="Model descriptor from `llama model list`",
    )
    quantization: Optional[QuantizationConfig] = None
    torch_seed: Optional[int] = None
    max_seq_len: int
    max_batch_size: int = 1

    @field_validator("model")
    @classmethod
    def validate_model(cls, model: str) -> str:
        permitted_models = [
            m.descriptor()
            for m in all_registered_models()
            if m.model_family == ModelFamily.llama3_1
        ]
        if model not in permitted_models:
            model_list = "\n\t".join(permitted_models)
            raise ValueError(
                f"Unknown model: `{model}`. Choose from [\n\t{model_list}\n]"
            )
        return model
