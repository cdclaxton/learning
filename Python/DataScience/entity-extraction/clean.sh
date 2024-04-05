lmdb_folder=./data/lmdb
if [ -d ${lmdb_folder} ]; then
    echo "Deleting LMDB database"
    rm -rf ${lmdb_folder}
fi

token_count_file=./data/token-to-count.pickle
if [ -f ${token_count_file} ]; then
    echo "Deleting token-to-count Pickle file"
    rm ${token_count_file}
fi

sqlite_file=./data/sqlite.db
if [ -f ${sqlite_file} ]; then
    echo "Deleting temporary Sqlite database"
    rm ${sqlite_file}
fi

rm -f ./*.so
rm -rf ./build

rm -f ./positions_compiled_c.c
rm -f ./positions_compiled_c.html

rm -f ./adds_removes.c
rm -f ./adds_removes.html