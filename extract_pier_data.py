import pdfplumber
import pandas as pd
import re
import os
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def find_sand_island_piers(text):
    """Find mentions of Sand Island piers in the text"""
    piers = set()
    
    # Look for specific Sand Island pier mentions
    sand_island_patterns = [
        r'Sand\s+Island\s+Pier\s+(\d+[A-Z]?)',
        r'SI\s+Pier\s+(\d+[A-Z]?)',
        r'Sand\s+Island.*?Pier\s+(\d+[A-Z]?)',
    ]
    
    for pattern in sand_island_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            piers.add(f"Sand Island Pier {match}")
    
    # Also search for sections specifically about Sand Island
    sand_island_sections = re.finditer(r'Sand\s+Island.*?(?=\n\s*\n|\Z)', text, re.IGNORECASE | re.DOTALL)
    for section_match in sand_island_sections:
        section_text = section_match.group(0)
        # Look for pier numbers in Sand Island context
        pier_matches = re.findall(r'Pier\s+(\d+[A-Z]?)', section_text, re.IGNORECASE)
        for pier_num in pier_matches:
            piers.add(f"Sand Island Pier {pier_num}")
    
    # Clean up pier names (remove newlines)
    cleaned_piers = set()
    for pier in piers:
        cleaned = re.sub(r'\s+', ' ', pier.strip())
        cleaned_piers.add(cleaned)
    
    return sorted(list(cleaned_piers))

def find_commodities_and_values(text):
    """Find commodities and their associated values"""
    # Common commodity patterns
    commodities = []
    
    # Look for tables or lists with commodities
    # Pattern: commodity name followed by numbers (could be tons, TEUs, value, etc.)
    commodity_patterns = [
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+([\d,]+\.?\d*)\s*(tons?|TEUs?|containers?|\$|million|thousand)',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+([\d,]+\.?\d*)',
    ]
    
    # Common commodity keywords
    commodity_keywords = [
        'container', 'containers', 'cargo', 'freight', 'bulk', 'breakbulk',
        'automobile', 'vehicles', 'petroleum', 'oil', 'gas', 'coal', 'grain',
        'lumber', 'steel', 'machinery', 'electronics', 'textiles', 'food',
        'chemicals', 'fertilizer', 'cement', 'aggregate', 'sand', 'gravel'
    ]
    
    # Look for sections mentioning commodities
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line_lower = line.lower()
        for keyword in commodity_keywords:
            if keyword in line_lower:
                # Try to extract numbers from nearby lines
                for j in range(max(0, i-2), min(len(lines), i+3)):
                    num_match = re.search(r'([\d,]+\.?\d*)\s*(tons?|TEUs?|containers?|\$|million|thousand|MT|kg)', lines[j], re.IGNORECASE)
                    if num_match:
                        commodities.append({
                            'commodity': keyword.title(),
                            'value': num_match.group(1).replace(',', ''),
                            'unit': num_match.group(2) if len(num_match.groups()) > 1 else '',
                            'context': line[:100]
                        })
                        break
    
    return commodities

def extract_tables_from_pdf(pdf_path):
    """Extract tables from PDF which might contain pier/commodity data"""
    tables_data = []
    pdf_name = Path(pdf_path).name
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        if table and len(table) > 0:
                            # Check if table contains relevant keywords
                            table_text = str(table).lower()
                            if any(keyword in table_text for keyword in ['pier', 'berth', 'commodity', 'cargo', 'sand island', 'ton', 'teu', 'container']):
                                tables_data.append({
                                    'page': page_num + 1,
                                    'table': table,
                                    'pdf_name': pdf_name
                                })
    except Exception as e:
        print(f"Error extracting tables from {pdf_path}: {e}")
    return tables_data

def main():
    # Paths
    ref_docs_path = Path("Ref_Documents")
    excel_path = Path("Data/Sand_Island_Piers.xlsx")
    
    # Ensure Data directory exists
    excel_path.parent.mkdir(exist_ok=True)
    
    # Extract data from PDFs
    all_piers = set()
    all_commodities = []
    all_tables = []
    pdf_file = None  # Track current PDF file for source attribution
    
    pdf_files = list(ref_docs_path.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files")
    
    for pdf_file in pdf_files:
        print(f"\nProcessing {pdf_file.name}...")
        
        # Extract text
        text = extract_text_from_pdf(pdf_file)
        print(f"Extracted {len(text)} characters of text")
        
        # Find piers
        piers = find_sand_island_piers(text)
        print(f"Found {len(piers)} pier mentions: {piers}")
        all_piers.update(piers)
        
        # Extract tables
        tables = extract_tables_from_pdf(pdf_file)
        print(f"Found {len(tables)} relevant tables")
        all_tables.extend(tables)
        
        # Find commodities
        commodities = find_commodities_and_values(text)
        print(f"Found {len(commodities)} commodity mentions")
        all_commodities.extend(commodities)
    
    # Read existing Excel file or create new structure
    try:
        df = pd.read_excel(excel_path)
        print(f"\nExisting Excel file has {len(df)} rows and columns: {list(df.columns)}")
    except Exception as e:
        print(f"\nCould not read existing Excel file: {e}")
        print("Creating new structure...")
        df = pd.DataFrame()
    
    # Create updated data structure
    # Structure: Pier, Commodity, Value, Unit, Source
    
    updated_data = []
    
    # Add pier information (only Sand Island piers)
    sand_island_piers = [p for p in sorted(all_piers) if 'sand island' in p.lower() or 'si pier' in p.lower()]
    for pier in sand_island_piers:
        updated_data.append({
            'Pier': pier,
            'Commodity': '',
            'Value': '',
            'Unit': '',
            'Source': 'PDF Text Extraction'
        })
    
    # Add commodity information
    for commodity_info in all_commodities:
        updated_data.append({
            'Pier': '',
            'Commodity': commodity_info.get('commodity', ''),
            'Value': commodity_info.get('value', ''),
            'Unit': commodity_info.get('unit', ''),
            'Source': 'PDF Extraction'
        })
    
    # Process tables for more structured data
    for table_info in all_tables:
        table = table_info['table']
        if table and len(table) > 1:  # Has header and data
            # Try to identify columns
            header = table[0] if table[0] else []
            
            # Find column indices for key fields
            pier_col_idx = None
            commodity_col_idx = None
            value_col_idx = None
            unit_col_idx = None
            
            for i, col_header in enumerate(header):
                if col_header:
                    col_lower = str(col_header).lower()
                    if 'pier' in col_lower or 'berth' in col_lower:
                        pier_col_idx = i
                    elif 'commodity' in col_lower or 'cargo' in col_lower or 'type' in col_lower:
                        commodity_col_idx = i
                    elif any(kw in col_lower for kw in ['ton', 'teu', 'value', 'volume', 'amount', 'quantity']):
                        value_col_idx = i
                    elif 'unit' in col_lower:
                        unit_col_idx = i
            
            # Check if table header mentions Sand Island (to process all rows)
            header_text = ' '.join([str(h) for h in header if h]).lower()
            is_sand_island_table = 'sand island' in header_text or 'si ' in header_text
            
            # Process rows
            for row in table[1:]:
                if row and len(row) > 0:
                    row_text = ' '.join([str(cell) for cell in row if cell]).lower()
                    
                    # Check if this row is about Sand Island or if table is Sand Island related
                    is_sand_island_row = ('sand island' in row_text or 'si ' in row_text or 
                                         is_sand_island_table or
                                         (pier_col_idx is not None and pier_col_idx < len(row) and 
                                          row[pier_col_idx] and 'sand island' in str(row[pier_col_idx]).lower()))
                    
                    if is_sand_island_row:
                        pier = ''
                        commodity = ''
                        value = ''
                        unit = ''
                        
                        # Extract pier - check all columns if not found in pier column
                        if pier_col_idx is not None and pier_col_idx < len(row) and row[pier_col_idx]:
                            pier_val = str(row[pier_col_idx]).strip()
                            if 'sand island' in pier_val.lower() or 'si ' in pier_val.lower():
                                pier = pier_val
                            elif re.match(r'^\d+[A-Z]?$', pier_val):
                                pier = f"Sand Island Pier {pier_val}"
                            elif pier_val:
                                pier = pier_val
                        
                        # If no pier found in pier column, check all columns for pier numbers
                        if not pier:
                            for i, cell in enumerate(row):
                                if cell:
                                    cell_str = str(cell).strip()
                                    # Check if it's a pier number
                                    if re.match(r'^\d+[A-Z]?$', cell_str) and i < len(header):
                                        col_header = str(header[i]).lower() if i < len(header) else ''
                                        if 'pier' in col_header or 'berth' in col_header:
                                            pier = f"Sand Island Pier {cell_str}"
                                            break
                        
                        # Extract commodity - check commodity column and other columns
                        if commodity_col_idx is not None and commodity_col_idx < len(row) and row[commodity_col_idx]:
                            commodity = str(row[commodity_col_idx]).strip()
                        
                        # If no commodity in commodity column, check other columns for commodity keywords
                        if not commodity:
                            commodity_keywords = ['container', 'cargo', 'freight', 'petroleum', 'oil', 'gas', 
                                                 'coal', 'grain', 'lumber', 'steel', 'machinery', 'automobile',
                                                 'cement', 'aggregate', 'sand', 'gravel', 'chemical']
                            for i, cell in enumerate(row):
                                if cell:
                                    cell_str = str(cell).strip().lower()
                                    if any(kw in cell_str for kw in commodity_keywords):
                                        commodity = str(cell).strip()
                                        break
                        
                        # Extract value - check value column and numeric columns
                        if value_col_idx is not None and value_col_idx < len(row) and row[value_col_idx]:
                            val_str = str(row[value_col_idx]).strip()
                            num_match = re.search(r'([\d,]+\.?\d*)', val_str.replace(',', ''))
                            if num_match:
                                value = num_match.group(1)
                            
                            # Try to extract unit from column header
                            if value_col_idx < len(header) and header[value_col_idx]:
                                header_lower = str(header[value_col_idx]).lower()
                                unit_match = re.search(r'(tons?|teus?|containers?|\$|million|thousand|mt|kg|mtons?)', header_lower)
                                if unit_match:
                                    unit = unit_match.group(1)
                        
                        # If no value found, check other numeric columns
                        if not value:
                            for i, cell in enumerate(row):
                                if cell:
                                    cell_str = str(cell).strip()
                                    num_match = re.search(r'^([\d,]+\.?\d*)\s*(tons?|teus?|containers?|million|thousand|mt|kg)?', cell_str, re.IGNORECASE)
                                    if num_match:
                                        value = num_match.group(1).replace(',', '')
                                        if num_match.group(2):
                                            unit = num_match.group(2)
                                        break
                        
                        # Extract unit if separate column
                        if unit_col_idx is not None and unit_col_idx < len(row) and row[unit_col_idx]:
                            unit = str(row[unit_col_idx]).strip()
                        
                        # Only add if we have meaningful data
                        if pier or (commodity and value):
                            updated_data.append({
                                'Pier': pier if pier else '',
                                'Commodity': commodity if commodity else '',
                                'Value': value if value else '',
                                'Unit': unit if unit else '',
                                'Source': f"Table from {table_info.get('pdf_name', 'PDF')} (Page {table_info['page']})"
                            })
    
    # Create DataFrame from updated data
    if updated_data:
        new_df = pd.DataFrame(updated_data)
        
        # Merge with existing data if it exists
        if not df.empty:
            # Combine dataframes
            combined_df = pd.concat([df, new_df], ignore_index=True)
            # Remove duplicates
            combined_df = combined_df.drop_duplicates()
        else:
            combined_df = new_df
        
        # Save to Excel - try with a temporary name first, then rename
        temp_excel_path = excel_path.parent / f"temp_{excel_path.name}"
        try:
            combined_df.to_excel(temp_excel_path, index=False)
            # Try to replace the original file
            if excel_path.exists():
                try:
                    excel_path.unlink()
                except PermissionError:
                    print(f"\nWARNING: Could not overwrite {excel_path} - file may be open in Excel.")
                    print(f"Data saved to {temp_excel_path} instead.")
                    print("Please close the Excel file and run the script again, or manually copy the data.")
                    return
            temp_excel_path.rename(excel_path)
            print(f"\nUpdated Excel file saved with {len(combined_df)} rows")
        except PermissionError:
            print(f"\nWARNING: Permission denied. The Excel file may be open.")
            print(f"Data saved to {temp_excel_path} instead.")
            print("Please close the Excel file and manually copy the data, or run the script again.")
            return
        
        print(f"\nColumns: {list(combined_df.columns)}")
        print(f"\nFirst few rows:")
        print(combined_df.head(20).to_string())
    else:
        print("\nNo data extracted. Please check the PDFs for relevant content.")
    
    # Print summary
    print(f"\n=== SUMMARY ===")
    print(f"Total unique piers found: {len(all_piers)}")
    print(f"Total commodity mentions: {len(all_commodities)}")
    print(f"Total relevant tables: {len(all_tables)}")

if __name__ == "__main__":
    main()

