from enum import Enum


class SymbolType(str, Enum):
    # Tipos primitivos — mapeados dos type keywords da linguagem
    REAL = "FP"        # floating point (real)
    INTEGER = "IN"
    STRING = "ST"
    CHARACTER = "CH"
    BOOLEAN = "BL"
    VOID = "VD"

    # Tipos array
    ARRAY_REAL = "AF"
    ARRAY_INTEGER = "AI"
    ARRAY_STRING = "AS"
    ARRAY_CHARACTER = "AC"
    ARRAY_BOOLEAN = "AB"
