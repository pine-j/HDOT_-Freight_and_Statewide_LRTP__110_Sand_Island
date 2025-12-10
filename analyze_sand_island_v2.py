import pdfplumber
import pandas as pd
import re
from pathlib import Path
import os

def extract_text_and_tables(pdf_path):
    text_content = []
    tables_content = []
    
    print(f"Processing {pdf_path}...")
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            # Extract text
            text = page.extract_text()
            if text:
                text_content.append({"page": i+1, "text": text, "pdf": pdf_path.name})
            
            # Extract tables
            tables = page.extract_tables()
            for table in tables:
                if table:
                    # Clean table: remove empty rows/cols
                    cleaned_table = [[cell.strip() if cell else "" for cell in row] for row in table]
                    # Filter out empty tables
                    if any(any(cell for cell in row) for row in cleaned_table):
                         tables_content.append({"page": i+1, "table": cleaned_table, "pdf": pdf_path.name})
    
    return text_content, tables_content

def analyze_piers(text_content):
    """
    Q1: What are the different piers in Sand Island port?
    Look for explicit mentions of Pier numbers associated with Sand Island.
    """
    piers = set()
    pier_details = []
    
    # Regex for Sand Island Piers: "Pier 51", "Piers 51-53", "Sand Island Pier 52"
    # Adjusted to capture ranges and specific numbers often found in Hawaii port docs
    patterns = [
        r"(?:Sand\s+Island|SI)\s+(?:Container\s+Terminal|Terminal)?\s*(?:Piers?|Berths?)\s+([0-9]+(?:-[0-9]+)?(?:[A-Z])?(?:\s*and\s*[0-9]+[A-Z]?)?)",
        r"(?:Piers?|Berths?)\s+([0-9]+(?:-[0-9]+)?(?:[A-Z])?)\s+(?:at|in|on)\s+Sand\s+Island"
    ]
    
    for entry in text_content:
        text = entry["text"]
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                pier_ref = match.group(1)
                full_match = match.group(0)
                # Clean up the pier reference
                clean_ref = pier_ref.replace('\n', ' ').strip()
                
                # Context extraction (sentence containing the match)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 100)
                context = text[start:end].replace('\n', ' ')
                
                if clean_ref not in piers:
                    piers.add(clean_ref)
                    pier_details.append({
                        "Pier Reference": clean_ref,
                        "Full Mention": full_match,
                        "Source File": entry["pdf"],
                        "Page": entry["page"],
                        "Context": "..." + context + "..."
                    })
    
    return pd.DataFrame(pier_details)

def analyze_commodities(text_content, tables_content):
    """
    Q2: What are the commodities that are traded in Sand Island?
    Look for commodity keywords and tables.
    """
    commodity_keywords = [
        "container", "breakbulk", "bulk", "petroleum", "oil", "gas", "automobile", "vehicle", "ro-ro",
        "cement", "sand", "gravel", "coal", "fertilizer", "livestock", "lumber", "steel", "grain", "food"
    ]
    
    extracted_data = []
    
    # Strategy 1: Look for tables with "Commodity" or "Cargo" in header
    for entry in tables_content:
        table = entry["table"]
        if not table: continue
        
        # Check headers
        headers = [str(cell).lower() for cell in table[0]]
        header_text = " ".join(headers)
        
        has_commodity = any(x in header_text for x in ["commodity", "cargo", "freight", "product"])
        has_value = any(x in header_text for x in ["ton", "value", "teu", "volume", "quantity"])
        
        # Also check if table mentions Sand Island or Harbors nearby
        table_str = str(table).lower()
        relevant_context = "sand island" in table_str or "honolulu harbor" in table_str
        
        if (has_commodity and has_value) or (has_commodity and relevant_context):
            # Try to extract rows
            cmd_idx = -1
            val_idx = -1
            
            for i, h in enumerate(headers):
                if any(x in h for x in ["commodity", "cargo", "type"]):
                    cmd_idx = i
                elif any(x in h for x in ["ton", "value", "teu", "volume"]):
                    val_idx = i
            
            if cmd_idx != -1:
                for row in table[1:]:
                    if len(row) > cmd_idx and row[cmd_idx]:
                        commodity = row[cmd_idx].strip()
                        value = row[val_idx].strip() if val_idx != -1 and len(row) > val_idx else "N/A"
                        
                        # Validate row
                        # Check if commodity text looks like a real commodity (not long sentence)
                        is_valid_text = len(commodity) < 50 and len(commodity) > 2
                        
                        # Check if it contains keywords
                        is_known_commodity = any(k in commodity.lower() for k in commodity_keywords)
                        
                        # Check if value looks numeric (if we have a value column)
                        has_numeric_value = False
                        if value != "N/A":
                             has_numeric_value = any(c.isdigit() for c in value)
                        
                        # Filter out non-commodity rows (totals, subtotals, unrelated text)
                        if is_valid_text and (is_known_commodity or has_numeric_value) and "total" not in commodity.lower():
                            extracted_data.append({
                                "Commodity": commodity,
                                "Value/Volume": value,
                                "Source Type": "Table",
                                "Source File": entry["pdf"],
                                "Page": entry["page"]
                            })

    # Strategy 2: Text search for lists of commodities
    # "Major commodities include...", "Top imports are...", etc.
    text_patterns = [
        r"(?:major|top|key)\s+(?:commodities|imports|exports|cargo)\s+(?:include|are|consist of)\s+([^.]+)",
        r"(?:commodities|cargo)\s+(?:handled|processed)\s+(?:at|in)\s+(?:Sand\s+Island|the\s+port|Honolulu)\s+(?:include|are)\s+([^.]+)"
    ]
    
    for entry in text_content:
        text = entry["text"]
        for pattern in text_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                content = match.group(1)
                # Clean and split content
                items = re.split(r',| and ', content)
                for item in items:
                    item = item.strip()
                    if len(item) > 2 and len(item) < 50:
                        extracted_data.append({
                            "Commodity": item,
                            "Value/Volume": "See context",
                            "Source Type": "Text Mention",
                            "Source File": entry["pdf"],
                            "Page": entry["page"],
                            "Context": match.group(0)
                        })

    return pd.DataFrame(extracted_data).drop_duplicates()

def analyze_countries(text_content):
    """
    Q3: What are the countries that trade with Sand Island?
    """
    # Common trading partners for Hawaii
    common_partners = [
        "Japan", "China", "South Korea", "Vietnam", "Taiwan", "Philippines", "Singapore",
        "Indonesia", "Thailand", "Malaysia", "Australia", "New Zealand", "Canada"
    ]
    
    found_partners = []
    
    for entry in text_content:
        text = entry["text"]
        # Look for sentences mentioning trade partners
        sentences = re.split(r'[.!?]', text)
        for sentence in sentences:
            if "trade" in sentence.lower() or "import" in sentence.lower() or "export" in sentence.lower():
                for country in common_partners:
                    if country in sentence:
                        found_partners.append({
                            "Country": country,
                            "Context": sentence.strip(),
                            "Source File": entry["pdf"],
                            "Page": entry["page"]
                        })
    
    return pd.DataFrame(found_partners).drop_duplicates()

def analyze_pier_commodities(text_content):
    """
    Q4: Do we have information per pier on what commodities are traded by a particular pier?
    Map Pier -> Commodities
    """
    mappings = []
    
    # Patterns like "Pier 51 handles containers" or "Automobiles at Pier 52"
    patterns = [
        r"(Pier\s+[0-9]+[A-Z]?)\s+(?:handles|processes|receives|ships|is used for)\s+([^.]+)",
        r"([^.]+)at\s+(Pier\s+[0-9]+[A-Z]?)"
    ]
    
    for entry in text_content:
        text = entry["text"]
        # Look for proximity of "Pier X" and commodity keywords
        lines = text.split('\n')
        for line in lines:
            if "Pier" in line and "Sand Island" in text: # Loose check for page context
                 # Check for Pier numbers
                 pier_matches = re.findall(r"Pier\s+([0-9]+[A-Z]?)", line)
                 if pier_matches:
                     for pier in pier_matches:
                         # Look for commodities in the same line
                         found_commodities = []
                         keywords = ["container", "auto", "vehicle", "bulk", "cement", "oil", "freight"]
                         for kw in keywords:
                             if kw in line.lower():
                                 found_commodities.append(kw)
                         
                         if found_commodities:
                             mappings.append({
                                 "Pier": f"Pier {pier}",
                                 "Commodities": ", ".join(found_commodities),
                                 "Raw Text": line.strip(),
                                 "Source File": entry["pdf"],
                                 "Page": entry["page"]
                             })

    return pd.DataFrame(mappings).drop_duplicates()

def main():
    ref_docs_path = Path("Ref_Documents")
    pdf_files = list(ref_docs_path.glob("*.pdf"))
    
    all_text = []
    all_tables = []
    
    for pdf in pdf_files:
        t, tbl = extract_text_and_tables(pdf)
        all_text.extend(t)
        all_tables.extend(tbl)
        
    print("Analyzing Piers...")
    df_piers = analyze_piers(all_text)
    
    print("Analyzing Commodities...")
    df_commodities = analyze_commodities(all_text, all_tables)
    
    print("Analyzing Trade Partners...")
    df_partners = analyze_countries(all_text)
    
    print("Analyzing Pier-Commodity Mappings...")
    df_pier_map = analyze_pier_commodities(all_text)
    
    # Save to Excel with multiple sheets
    output_path = Path("Data/Sand_Island_Analysis.xlsx")
    output_path.parent.mkdir(exist_ok=True)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        if not df_piers.empty:
            df_piers.to_excel(writer, sheet_name='Piers', index=False)
        else:
            pd.DataFrame({"Message": ["No explicit pier lists found"]}).to_excel(writer, sheet_name='Piers', index=False)
            
        if not df_commodities.empty:
            df_commodities.to_excel(writer, sheet_name='Commodities', index=False)
        else:
             pd.DataFrame({"Message": ["No commodity tables found"]}).to_excel(writer, sheet_name='Commodities', index=False)

        if not df_partners.empty:
            df_partners.to_excel(writer, sheet_name='Trade_Partners', index=False)
        else:
             pd.DataFrame({"Message": ["No trade partners found"]}).to_excel(writer, sheet_name='Trade_Partners', index=False)

        if not df_pier_map.empty:
            df_pier_map.to_excel(writer, sheet_name='Pier_Usage', index=False)
        else:
             pd.DataFrame({"Message": ["No pier-commodity mapping found"]}).to_excel(writer, sheet_name='Pier_Usage', index=False)

    print(f"\nAnalysis saved to {output_path}")
    print("Summary:")
    print(f"Piers found: {len(df_piers)}")
    print(f"Commodity rows: {len(df_commodities)}")
    print(f"Partners found: {len(df_partners)}")
    print(f"Pier Usage mappings: {len(df_pier_map)}")

if __name__ == "__main__":
    main()

