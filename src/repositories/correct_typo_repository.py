import difflib


class CorrectTypo:
    def get_close_matches(self, out_result, container, typo):
        out_result.update(difflib.get_close_matches(typo, container))
        if hasattr(container, "values"):
            for inner in container.values():
                self.get_close_matches(out_result, inner, typo)
