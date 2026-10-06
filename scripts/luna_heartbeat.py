"""Luna-only compatibility launcher over the existing Hamut'ay heartbeat.

Explicit non-strict function schemas preserve omitted optional selectors on
this OpenRouter route. Mechanical live validation is recorded in the operation
notes. No authored state or tool parameters are rewritten by this adapter.
"""
from copy import deepcopy
from hamutay.taste_open import OpenAITasteBackend


class LunaTasteBackend(OpenAITasteBackend):
    @staticmethod
    def _openai_tool_def(tool):
        definition = deepcopy(OpenAITasteBackend._openai_tool_def(tool))
        definition['function']['strict'] = False
        return definition


def main():
    import hamutay.heartbeat as heartbeat
    import hamutay.taste_open as taste_open
    args = heartbeat.build_parser().parse_args()
    if args.provider != 'openrouter' or args.model != 'openai/gpt-6-luna':
        raise SystemExit('This compatibility launcher requires --provider openrouter --model openai/gpt-6-luna.')
    # build_session imports this backend at call time. Process-local only;
    # other resident processes and the shared checkout are unchanged.
    taste_open.OpenAITasteBackend = LunaTasteBackend
    heartbeat.main()


if __name__ == '__main__':
    main()
