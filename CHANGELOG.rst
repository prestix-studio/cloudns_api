.. :changelog:

Release History
---------------

0.9 (May 5, 2020)
+++++++++++++++++

* Version 1 Release candidate.
* Adds support for checking if a DNS zone is updated (`is_updated`).
* Updates error handling in `publish` script.


0.8 (April 2, 2020)
+++++++++++++++++++

* Fourth Beta Release.
* Adds support for TLSA records.
* Minor fixes and tweaks to documentation for clarification.
* Fixes a bug where tests required auth environment variables to be set in
  order to run successfully.


0.7 (November 16, 2019)
+++++++++++++++++++++++

* Third Beta Release.
* Adds DNS Support for zones (Thanks to
  `kristinn <https://github.com/kristinn>`__).
* Allows authentication with sub-users through environment variables
  'CLOUDNS_API_SUB_AUTH_ID' or 'CLOUDNS_API_SUB_AUTH_USER'. (Thanks to
  `sadimusi <https://github.com/sadimusi>`__).


0.6 (September 14, 2019)
++++++++++++++++++++++++

* Second Beta Release.
* Corrects wrong bash variable 'CLOUDNS_API_AUTH_USER' to 'CLOUDNS_API_AUTH_ID'
  in README.rst
* Changes the way errors are thrown when auth environment variables are not
  set. This allows the library to be included without these variables without
  immediately throwing an error. Now the error is only thrown when they are
  needed to authenticate.


0.5 (July 13, 2019)
+++++++++++++++++++

* Beta Release.
* Updates github address to Prestix Studio, LLC github account.
* Corrects pypi reference.
* Adds publish script to push next version to pypi automatically.
* Minor code cleanup.


0.4 (July 07, 2019)
+++++++++++++++++++

* Alpha Release - all mvp features.
* Minor bugfixes from v0.3.


0.3 (June 05, 2019)
+++++++++++++++++++

* Planning/Testing Release 'b' - updates to core modules.


0.2 (September 19, 2018)
++++++++++++++++++++++++

* Planning/Testing Release 'a' - adds some real code for initial testing.


0.1 (September 16, 2018)
++++++++++++++++++++++++

* Initial Planning Release to secure 'cloudns-api' name.
