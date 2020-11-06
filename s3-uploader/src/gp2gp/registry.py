class ProcessedFileRegistry:
    def __init__(self, conn):
        self._conn = conn
        self._table_initialised = False

    def _init_table(self):
        if not self._table_initialised:
            self._conn.execute(
                (
                    "CREATE TABLE IF NOT EXISTS processed_files "
                    "(filename string, bucket string, UNIQUE(filename, bucket))"
                )
            )
            self._table_initialised = True

    def is_already_processed(self, file, s3_bucket):
        self._init_table()
        query = self._conn.execute(
            "SELECT * FROM processed_files WHERE filename=? AND bucket=?",
            (str(file.path), s3_bucket),
        )
        return query.fetchone() is not None

    def mark_processed(self, file, s3_bucket):
        self._init_table()
        self._conn.execute("INSERT INTO processed_files VALUES (?, ?)", (str(file.path), s3_bucket))
        self._conn.commit()