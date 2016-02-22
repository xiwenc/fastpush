FastPush: Update Cloud Foundry/Heroku application in seconds
==

> Why should your development environment be any different from your production environment except for the number of instances?

*FastPush* enables developers to push incremental updates of your application to [Cloud Foundry](https://www.cloudfoundry.org)/[Heroku](https://www.heroku.com). In addition to pushing incremental updates it detects whether it is necessary to restart the application for the new changes to have effect. As a result updating your application takes *seconds* instead of *minutes*.

During Cloud Foundry Summit Berlin 2015 [Jouke](https://github.com/jtwaleson) and [Xiwen](https://github.com/xiwenc) had an eureka moment on how to speed up deployment speed of apps. The original idea was first brought up by Jouke because we were challenged to make application deployments faster at [Mendix](https://www.mendix.com) which adopted Cloud Foundry. At the conference we were inspired by the community and [Cloud Rocker](https://github.com/CloudCredo/cloudrocker). With *FastPush* we solve somewhat the same problem as *Cloud Rocker* namely: how to develop applications at a faster pace by shortening the feedback loop. Cloud Rocker enables developers to run their application locally using *Docker*. *FastPush* shortens deployment time to a real Cloud Foundry cluster by efficiently synchronizing changed files *without restaging* the application. This way we can still leverage all the goodies of CF like publicly accessible and the rich services ecosystem.

Developers and Designers love FastPush because small changes in the source code can be deployed almost instantly without the need to run supporting services locally. Just like how Cloud Foundry/Heroku revolutionized deployment of applications we hope to bring this revolution closer into the development process.

> Current documentation is fairly low because this project is still very young. We invite others to contribute. The code quality is not great either and we plan to refactor it in the near future. Please keep in mind the current state is far from production ready but for its purpose it is good enough to be used as a developer tool ;)

Related projects
===

- [fastpush](https://github.com/xiwenc/fastpush) (this repo) FastPush documentation with integration examples
- [cf-fastpush-controller](https://github.com/xiwenc/cf-fastpush-controller) FastPush server written in Go that can be included in your application root directory
- [cf-fastpush-plugin](https://github.com/xiwenc/cf-fastpush-plugin) FastPush client plugin for Cloud Foundry CLI

Disclaimer
===

- FastPush is lightning fast because it skips the staging phase in Cloud Foundry for subsequent changes. This means that `cf fast-push` cannot and will never replace the standard `cf push` command.
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

How it works
===

The fastpush mechanism uses the server-client model. The server is `cf-fastpush-controller` and the client is a cf cli plugin `cf-fastpush-plugin`.

- `cf-fastpush-controller`: A daemon that sits between your application and the gorouters. This service is always available and it responds to some specific paths under `/_fastpush/`. Paths that are not known to the controller are reverse-proxied to the backend application which is your application. It keeps track of your remote files and accepts new and existing files. Depending on what files has changed it can trigger an automatic restart of the backend.
- `cf-fastpush-plugin`: A cf cli plugin that talks to the controller. It tracks your local files and synchronizes those that has been changed or added.

The actual code does more than what is documented here. So we suggest you to read the source if you are really interested in how it works and what else it can do.


Credits:
===
- Mendix: Great place to work
- Colleagues @ Mendix
