from __future__ import annotations
import argparse, pandas as pd
from pathlib import Path
from utils import ensure_schema, insert_session

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def main():
    ap=argparse.ArgumentParser(description='Ingest CSV into SQLite')
    ap.add_argument('--csv',default=PROJECT_ROOT/'database'/'data'/'sessions.csv'); ap.add_argument('--db',default=PROJECT_ROOT/'database'/'data'/'study.db'); ap.add_argument('--schema',default=PROJECT_ROOT/'database'/'sql'/'schema.sql')
    ap.add_argument('--user_id', type=int, default=1, help='User ID to assign sessions to')
    args=ap.parse_args()
    db=Path(args.db); schema=Path(args.schema); db.parent.mkdir(parents=True, exist_ok=True); ensure_schema(db, schema)
    df=pd.read_csv(args.csv)
    for _,r in df.iterrows():
        insert_session(db, {'date':r['date'],'start_time':r['start_time'],'end_time':r['end_time'],'subject':r['subject'],'technique':r['technique'],'distractions':int(r['distractions']),'mood':int(r['mood']),'caffeine_mg':int(r['caffeine_mg']),'productivity':int(r['productivity'])}, args.user_id)
    print(f'Ingested {len(df)} rows -> {db} for user_id={args.user_id}')
if __name__=='__main__': main()
