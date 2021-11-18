from people import Person
from util.log import log

if __name__ == '__main__':
    import sys

    person = Person(name=sys.argv[1], pwd=sys.argv[2])
    todayOk, res, err = person.report()
    log("res:"+str(todayOk or res)+",err:"+err)