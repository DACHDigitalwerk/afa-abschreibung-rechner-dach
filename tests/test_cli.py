# -*- coding: utf-8 -*-
"""
Unit tests for afa_dach.cli (dach-afa command).
"""

import io
import json
import contextlib
import pytest
from afa_dach.cli import run_cli


def test_cli_help():
    """Test CLI help screen returns 0."""
    buf_out = io.StringIO()
    buf_err = io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        code = run_cli(["--help"])
    assert code == 0
    assert "dach-afa" in buf_out.getvalue()


def test_cli_standard_linear():
    """Test standard CLI run with linear AfA."""
    buf_out = io.StringIO()
    buf_err = io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        code = run_cli([
            "--cost", "12000.0",
            "--years", "3",
            "--name", "Notebook Workstation",
            "--method", "linear"
        ])
    assert code == 0
    out = buf_out.getvalue()
    assert "Notebook Workstation" in out
    assert "12.000,00 €" in out
    assert "AfA im Anschaffungsjahr: 4.000,00 €" in out


def test_cli_degressiv_opt():
    """Test CLI run with degressiv-opt method and switch year."""
    buf_out = io.StringIO()
    buf_err = io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        code = run_cli([
            "--cost", "50000.0",
            "--years", "10",
            "--method", "degressiv-opt"
        ])
    assert code == 0
    out = buf_out.getvalue()
    assert "Optimaler Wechsel:      Jahr 7 (2032) zu linear" in out


def test_cli_json_output():
    """Test CLI output with --json flag."""
    buf_out = io.StringIO()
    buf_err = io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        code = run_cli([
            "--cost", "50000.0",
            "--years", "10",
            "--method", "degressiv-opt",
            "--json"
        ])
    assert code == 0
    data = json.loads(buf_out.getvalue())
    assert data["acquisition_cost"] == 50000.0
    assert data["useful_life_years"] == 10
    assert data["switch_year_index"] == 7
    assert len(data["schedule"]) == 10


def test_cli_austria_flag():
    """Test CLI with Austrian country flag."""
    buf_out = io.StringIO()
    buf_err = io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        code = run_cli([
            "--cost", "10000.0",
            "--years", "5",
            "--month", "8",
            "--method", "linear",
            "--country", "AT",
            "--json"
        ])
    assert code == 0
    data = json.loads(buf_out.getvalue())
    assert data["country"] == "AT"
    # Month 8 (>6) -> half year AfA in year 1
    assert data["schedule"][0]["total_yearly_afa"] == 1000.0


def test_cli_switzerland_flag():
    """Test CLI with Swiss country flag."""
    buf_out = io.StringIO()
    buf_err = io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        code = run_cli([
            "--cost", "25000.0",
            "--years", "5",
            "--country", "CH",
            "--json"
        ])
    assert code == 0
    data = json.loads(buf_out.getvalue())
    assert data["country"] == "CH"
    assert data["currency"] == "CHF"


def test_cli_sonderafa_flag():
    """Test CLI with § 7g Sonder-AfA flag."""
    buf_out = io.StringIO()
    buf_err = io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        code = run_cli([
            "--cost", "20000.0",
            "--years", "5",
            "--sonderafa", "20.0",
            "--method", "linear",
            "--json"
        ])
    assert code == 0
    data = json.loads(buf_out.getvalue())
    assert data["schedule"][0]["sonder_afa"] == 4000.0
    assert data["schedule"][0]["total_yearly_afa"] == 8000.0


def test_cli_validation_failure():
    """Test CLI returns 1 on invalid argument values."""
    buf_out = io.StringIO()
    buf_err = io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        code = run_cli([
            "--cost", "-100.0",
            "--years", "5"
        ])
    assert code == 1
    assert "Fehler" in buf_err.getvalue()
