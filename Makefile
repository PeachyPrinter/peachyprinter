.PHONY: po mo

po:
	xgettext -Lpython --output=src/resources/il8n/messages.pot src/main.py src/peachyprinter.kv test/infrastructure_test/langtoolstest.py src/infrastructure/setting_mapper.py
	msgmerge --update --no-fuzzy-matching --backup=off src/resources/il8n/po/en_GB.po src/resources/il8n/messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off src/resources/il8n/po/en_US.po src/resources/il8n/messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off src/resources/il8n/po/tlh.po src/resources/il8n/messages.pot

mo:
	mkdir -p src/resources/il8n/locales/en_GB/LC_MESSAGES
	mkdir -p src/resources/il8n/locales/en_US/LC_MESSAGES
	mkdir -p src/resources/il8n/locales/tlh/LC_MESSAGES
	msgfmt -c -o src/resources/il8n/locales/en_GB/LC_MESSAGES/peachyprinter.mo src/resources/il8n/po/en_GB.po
	msgfmt -c -o src/resources/il8n/locales/en_US/LC_MESSAGES/peachyprinter.mo src/resources/il8n/po/en_US.po
	msgfmt -c -o src/resources/il8n/locales/tlh/LC_MESSAGES/peachyprinter.mo src/resources/il8n/po/tlh.po
