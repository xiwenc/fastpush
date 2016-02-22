FastPush: Push updates to Cloud Foundry/Heroku apps in seconds
==

> Why should your development environment be any different from your production environment except for the number of instances?

*FastPush* allows you to instantly push updates of your code to [Cloud Foundry](https://www.cloudfoundry.org)/[Heroku](https://www.heroku.com). If static files have changed, it just syncs those. If code has changed, it also restarts the app. As a result updating your application takes *seconds* instead of *minutes*. So no more getting coffee while waiting for `cf push` and more importantly, your *flow* won't be interrupted.

Pros:
- never install local database, message brokers, email providers etc., simply use the Free Tiers of the 3rd party providers on Heroku / Cloud Foundry
- eliminate differences between dev & prod, no more `port = (env.process.PORT || 5000)`

Cons:
- unable to work offline
- app reverts to last pushed version when restarted
- still need full push when dependencies change


How does it work
===

We add a small http proxy (`cf-fastpush-controller`, written in Go) between the app's http port and the PaaS routing layer. This http proxy just proxies everything to the application, except that it has a file synchronization api listening on `/_fastpush/`. This allows us to modify the live file system of the container.

We transfer local files to the server with the `cf-fastpush-plugin`, a cf cli plugin that talks to the controller. It tracks your local files and synchronizes those that have been changed or added.

The actual code does more than what is documented here. So we suggest you to read the source if you are really interested in how it works and what else it can do.

> Current documentation is fairly low because this project is still very young. We invite others to contribute. The code quality is not great either and we plan to refactor it in the near future. Please keep in mind the current state is far from production ready but for its purpose it is good enough to be used as a developer tool ;)

Related projects
===

- [fastpush](https://github.com/xiwenc/fastpush) (this repo) FastPush documentation with integration examples
- [cf-fastpush-controller](https://github.com/xiwenc/cf-fastpush-controller) FastPush server written in Go that can be included in your application root directory
- [cf-fastpush-plugin](https://github.com/xiwenc/cf-fastpush-plugin) FastPush client plugin for Cloud Foundry CLI

Disclaimer
===

- FastPush is lightning fast because it skips the `staging` phase in Cloud Foundry for subsequent changes. This means that `cf fast-push` cannot and will never replace the standard `cf push` command.
- FastPush *does not* work with multi-instance deployments
- FastPush should *never* be used to deploy production applications

Usage
===

It is extremely easy to start using *FastPush*:

1. Build and include [cf-fastpush-controller](https://github.com/xiwenc/cf-fastpush-controller) executable in your application code.
2. Build and install [cf-fastpush-plugin](https://github.com/xiwenc/cf-fastpush-plugin) in your CF CLI. As of this writing there is no Heroku plugin yet.
3. Modify your `manifest.yml` to configure your application and `cf-fastpush-controller`.
4. After your first `cf push` you can incrementally push updates with `cf fast-push`.

Cloud Foundry Tutorial
===

For those that are still confused why *FastPush* is such an awesome tool just follow this short step-by-step tutorial where we deploy an example application:

```bash
# Install cf-fastpush-plugin
wget https://github.com/xiwenc/cf-fastpush-plugin/raw/master/cf-fastpush-plugin
chmod 755 cf-fastpush-plugin
cf install-plugin cf-fastpush-plugin
rm cf-fastpush-plugin

# grab example app
git clone https://github.com/xiwenc/fastpush.git
# Here we choose python, but there are more examples
cd fastpush/examples/python

# Install cf-fastpush-controller
wget https://github.com/xiwenc/cf-fastpush-controller/raw/master/cf-fastpush-controller
chmod 755 cf-fastpush-controller

# Let's push our initial application
time cf push samplefastpush
# ... snip ...
# #0   running   2016-01-29 09:31:06 PM   0.0%   15.7M of 128M   114.9M of 256M
# ... snip ...
#cf push samplefastpush  1.88s user 1.91s system 5% cpu 1:04.55 total


# Now with fast push

# Change the file a bit
vim hello.py

# repush with fast-push
time cf fast-push samplefastpush
# ... snip ...
# [MOD] hello.py
# [NEW] manifest.yml
# Restarting after updating 2 files

# cf fast-push samplefastpush  0.40s user 0.05s system 7% cpu 5.667 total
```
Please note that the initial push is not very representative of a real world scenario because it adds overhead of having to push the cf-fastpush-controller binary. We can speed it up for slow connections by incorporating it in buildpacks that fetches the executable if needed.

Note: Feel free to submit Pull-requests for examples integrations with other frameworks/languages.


Credits:
===
- Mendix: Great place to work
- Colleagues @ Mendix
