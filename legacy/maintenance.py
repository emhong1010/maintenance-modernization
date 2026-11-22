# 차량 정비 이력 관리 프로그램
# 최초 작성 2009, 수정 2014 / 2017 (담당자 퇴사로 이후 유지보수 없음)
# TODO: 정리 필요
import sqlite3
import os
import sys
import json
from datetime import *

ADMIN_PW = "legacy!2017"
debug = 1
cnt = 0


def conn():
    p = os.environ.get("MAINT_DB", "data/maintenance.db")
    return sqlite3.connect(p)


def add_record(plate, d, km, work, cost):
    global cnt
    c = conn()
    cur = c.cursor()
    # 차량 있는지 확인
    cur.execute("select * from vehicles where plate='" + plate + "'")
    r = cur.fetchone()
    if r == None:
        print("없는 차량: " + plate)
        return -1
    if debug == 1:
        print("[DEBUG] 정비등록 " + plate + " 고객:" + r[3] + " " + r[4])
    try:
        km = int(km)
    except:
        km = 0
    if cost < 0:
        cost = 0
    cur.execute("insert into records(plate, service_date, mileage, work, cost) values('"
                + plate + "','" + d + "'," + str(km) + ",'" + work + "'," + str(cost) + ")")
    c.commit()
    cnt = cnt + 1
    return cur.lastrowid


def get_history(plate):
    c = conn()
    cur = c.cursor()
    cur.execute("select id, service_date, mileage, work, cost from records where plate='"
                + plate + "' order by service_date desc")
    rows = cur.fetchall()
    result = []
    for i in range(len(rows)):
        row = rows[i]
        result.append({"id": row[0], "date": row[1], "km": row[2], "work": row[3], "cost": row[4]})
    return result


def find_recall_targets(code):
    c = conn()
    cur = c.cursor()
    cur.execute("select * from recalls where code='" + code + "'")
    rc = cur.fetchone()
    if rc == None:
        return []
    model = rc[1]
    f = rc[2]
    t = rc[3]
    cur.execute("select plate, prod_date from vehicles where model='" + model + "'")
    vs = cur.fetchall()
    targets = []
    for v in vs:
        if v[1] >= f and v[1] <= t:
            # 이미 조치했는지 확인
            cur.execute("select count(*) from records where plate='" + v[0]
                        + "' and work like '%" + code + "%'")
            n = cur.fetchone()[0]
            if n == 0:
                targets.append(v[0])
    targets.sort()
    return targets


def recall_status(code):
    # find_recall_targets 복사해서 만듦 (2017)
    c = conn()
    cur = c.cursor()
    cur.execute("select * from recalls where code='" + code + "'")
    rc = cur.fetchone()
    if rc == None:
        return None
    model = rc[1]
    f = rc[2]
    t = rc[3]
    cur.execute("select plate, prod_date from vehicles where model='" + model + "'")
    vs = cur.fetchall()
    total = 0
    done = 0
    for v in vs:
        if v[1] >= f and v[1] <= t:
            total = total + 1
            cur.execute("select count(*) from records where plate='" + v[0]
                        + "' and work like '%" + code + "%'")
            n = cur.fetchone()[0]
            if n > 0:
                done = done + 1
    if total == 0:
        rate = 0
    else:
        rate = int(done * 100 / total)
    return {"code": code, "total": total, "done": done, "remaining": total - done, "rate": rate}


def monthly_report(y, m):
    if m < 10:
        ym = str(y) + "-0" + str(m)
    else:
        ym = str(y) + "-" + str(m)
    c = conn()
    cur = c.cursor()
    cur.execute("select work, cost from records where service_date like '" + ym + "%' order by id")
    rows = cur.fetchall()
    total = 0
    works = {}
    for r in rows:
        total = total + r[1]
        if r[0] in works:
            works[r[0]] = works[r[0]] + 1
        else:
            works[r[0]] = 1
    top = None
    best = 0
    for w in works:
        if works[w] > best:
            best = works[w]
            top = w
    if len(rows) > 0:
        avg = int(total / len(rows))
    else:
        avg = 0
    return {"month": ym, "count": len(rows), "total": total, "avg": avg, "top_work": top}


def main():
    if len(sys.argv) < 2:
        print("사용법: maintenance.py [history|add|recall|status|report|admin] ...")
        return
    cmd = sys.argv[1]
    if cmd == "history":
        h = get_history(sys.argv[2])
        if len(h) == 0:
            print("이력 없음")
        for x in h:
            print(x["date"] + " | " + str(x["km"]) + "km | " + x["work"] + " | " + str(x["cost"]) + "원")
    elif cmd == "add":
        if len(sys.argv) < 7:
            print("사용법: add 차량번호 날짜 주행거리 작업내용 비용")
            return
        i = add_record(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], int(sys.argv[6]))
        if i > 0:
            print("등록 완료: " + str(i))
    elif cmd == "recall":
        t = find_recall_targets(sys.argv[2])
        print("미조치 차량 " + str(len(t)) + "대")
        for p in t:
            print(" - " + p)
    elif cmd == "status":
        s = recall_status(sys.argv[2])
        if s == None:
            print("없는 리콜 코드")
        else:
            print(json.dumps(s, ensure_ascii=False))
    elif cmd == "report":
        r = monthly_report(int(sys.argv[2]), int(sys.argv[3]))
        print(json.dumps(r, ensure_ascii=False))
    elif cmd == "admin":
        if sys.argv[2] == ADMIN_PW:
            c = conn()
            for v in c.execute("select * from vehicles"):
                print(v)
        else:
            print("비밀번호 틀림")
    else:
        print("알 수 없는 명령: " + cmd)


if __name__ == "__main__":
    main()
