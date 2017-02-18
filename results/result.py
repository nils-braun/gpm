from gpm.instances.instance import FileInstance


class ResultFolder:
    def __init__(self, state_db):
        self._state_db = state_db

    def store_results(self, output_file_name, state_hash):
        output_file_state = FileInstance(output_file_name).snapshot(self._state_db)
        output_file_hash = output_file_state.store(self._state_db)

        try:
            stored_state_content_pairs = self._state_db.get(output_file_name)
        except KeyError:
            stored_state_content_pairs = []

        stored_state_content_pairs.append((state_hash, output_file_hash))

        self._state_db.set(output_file_name, stored_state_content_pairs)

    def get_results(self, result_file_name):
        stored_state_content_pairs = self._state_db.get(result_file_name)

        for stored_state_content in stored_state_content_pairs:
            state_hash, output_file_hash = stored_state_content
            yield Commit(result_file_name, output_file_hash, state_hash)


class Commit:
    def __init__(self, file_name, file_content_hash, state_hash):
        self.file_name = file_name
        self.file_content_hash = file_content_hash
        self.state_hash = state_hash