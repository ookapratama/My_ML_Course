import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from typing import List, Set, Tuple


def run_analysis(input_xlsx_path: str, output_xlsx_path: str) -> None:
    """
    Menganalisis transaksi menggunakan algoritma Apriori dan menghasilkan rekomendasi paket produk.
    
    Args:
        input_xlsx_path: Path ke file Excel input dengan data transaksi
        output_xlsx_path: Path ke file Excel output untuk hasil paket produk
    """
    
    df = pd.read_excel(input_xlsx_path, sheet_name='Transaksi')
    print(f"Data loaded: {len(df)} rows")
    print(f"Unique transactions: {df['Kode Transaksi'].nunique()}")
    print(f"Unique products: {df['Nama Produk'].nunique()}")
    
    basket = df.groupby(['Kode Transaksi', 'Nama Produk'])['Nama Produk'].count().unstack().fillna(0)
    
    basket_sets = basket.applymap(lambda x: x > 0)
    
    print(f"\nBasket shape: {basket_sets.shape}")
    
    frequent_itemsets = apriori(basket_sets, min_support=0.05, use_colnames=True)
    print(f"Frequent itemsets found: {len(frequent_itemsets)}")
    
    if len(frequent_itemsets) == 0:
        print("No frequent itemsets found with min_support=0.05")
        pd.DataFrame(columns=['Packaging Set ID', 'Products', 'Maximum Lift', 'Maximum Confidence']).to_excel(output_xlsx_path, index=False)
        return
    
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.4)
    print(f"Association rules found: {len(rules)}")
    
    if len(rules) == 0:
        print("No association rules found with min_confidence=0.4")
        pd.DataFrame(columns=['Packaging Set ID', 'Products', 'Maximum Lift', 'Maximum Confidence']).to_excel(output_xlsx_path, index=False)
        return
    
    product_combinations = {}
    
    for idx, row in rules.iterrows():
        all_products = row['antecedents'].union(row['consequents'])
        
        sorted_products = tuple(sorted(all_products))
        
        if sorted_products not in product_combinations:
            product_combinations[sorted_products] = {
                'lift': row['lift'],
                'confidence': row['confidence']
            }
        else:
            if row['lift'] > product_combinations[sorted_products]['lift']:
                product_combinations[sorted_products]['lift'] = row['lift']
            if row['confidence'] > product_combinations[sorted_products]['confidence']:
                product_combinations[sorted_products]['confidence'] = row['confidence']
    
    output_data = []
    for products, metrics in product_combinations.items():
        output_data.append({
            'Products': ';'.join(products),
            'Maximum Lift': metrics['lift'],
            'Maximum Confidence': metrics['confidence']
        })
    
    df_output = pd.DataFrame(output_data)
    
    df_output = df_output.sort_values(
        by=['Maximum Lift', 'Maximum Confidence'], 
        ascending=[False, False]
    ).reset_index(drop=True)
    
    df_output.insert(0, 'Packaging Set ID', range(1, len(df_output) + 1))
    
    df_output.to_excel(output_xlsx_path, index=False)
    
    print(f"\n✓ Analysis complete!")
    print(f"✓ Output saved to: {output_xlsx_path}")
    print(f"✓ Total product packaging sets: {len(df_output)}")
    print(f"\nTop 5 combinations:")
    print(df_output.head().to_string(index=False))


if __name__ == "__main__":
    run_analysis("/home/ooka/BACKUP ARCH/jinx/Belajar/ML udemy/Beta Testing Hackathon DQLab/BETA-02/transaksi_dqmart.xlsx", "product_packaging.xlsx")