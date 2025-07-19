# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository implements a Model Context Protocol (MCP) server for the YOKATLAS API (Turkish Higher Education Atlas) using FastMCP. It provides programmatic access to Turkish university program data through MCP-compatible tools for LLMs like Claude Desktop.

## Common Development Tasks

### Running the MCP Server

The main server file is `yokatlas_mcp_server.py`. To run the server:

```bash
# Run with SSE transport (default in the script)
python yokatlas_mcp_server.py

# Run with FastMCP CLI
fastmcp run yokatlas_mcp_server.py
```

### Installing Dependencies

This project uses Python 3.12+ and manages dependencies through `pyproject.toml`:

```bash
# Install with uv (recommended)
uv pip install -e .

# Or install individual dependencies
uv pip install beautifulsoup4 fastmcp yokatlas-py setuptools
```

## Architecture

### Core Components

1. **yokatlas_mcp_server.py**: Main MCP server implementation
   - Creates a FastMCP server instance that exposes YOKATLAS API functions as MCP tools
   - Implements 4 main tools for accessing Turkish university program data
   - Uses async/await for YOKATLAS API calls

2. **Dependencies**:
   - `yokatlas-py`: Core library for accessing YOKATLAS data
   - `fastmcp`: Framework for building MCP servers
   - `beautifulsoup4`: HTML parsing (dependency of yokatlas-py)

### Available MCP Tools

1. **get_associate_degree_atlas_details**: Fetches details for associate degree programs
   - Parameters: `yop_kodu` (program ID), `year`
   - Returns comprehensive program data including quotas, statistics, and placement info

2. **get_bachelor_degree_atlas_details**: Fetches details for bachelor's degree programs
   - Parameters: `yop_kodu` (program ID), `year`
   - Returns comprehensive program data similar to associate degrees

3. **search_bachelor_degree_programs**: Searches bachelor's degree programs
   - Parameters include university name, program name, city, score type (SAY/EA/SOZ/DIL), ranking bounds
   - Returns paginated search results

4. **search_associate_degree_programs**: Searches associate degree programs
   - Parameters similar to bachelor's search but uses score bounds instead of ranking
   - Returns paginated search results

### Error Handling

All tools include try-except blocks that return error dictionaries with the error message and request parameters when exceptions occur.

## Integration with Claude Desktop

The server can be integrated with Claude Desktop either through:
1. `fastmcp install` command (recommended)
2. Manual configuration by editing `claude_desktop_config.json`

The server runs with uv for isolated Python environment management.