"""interface for app plugins."""
import abc


class AppPlugin():
    """Interface class for an application."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractstaticmethod
    def process_app_config(provider, name, cloud_config, app_config):
        """
        Validate and build an internal app config.

        Validate an application config entered by the user and builds a new
        processed dictionary of values which will be used by the launch_app
        method. Raises a ValidationError if the application configuration is
        invalid. This method must execute quickly and should not contain long
        running operations, and is designed to provide quick feedback on
        configuration errors to the client.

        @type  provider: :class:`CloudBridge.CloudProvider`
        @param provider: Cloud provider where the supplied app is to be
                         created.

        @type  name: ``str``
        @param name: Name for this deployment.

        @type  cloud_config: ``dict``
        @param cloud_config: A dict containing cloud infrastructure specific
                             configuration for this app.

        @type  app_config: ``dict``
        @param app_config: A dict containing the original, unprocessed version
                           of the app config. The app config is a merged dict
                           of database stored settings and user-entered
                           settings.

        :rtype: ``dict``
        :return: A ``dict` containing the launch configuration.
        """
        pass

    @abc.abstractstaticmethod
    def sanitise_app_config(app_config):
        """
        Sanitise values in the app_config.

        The returned representation should have all sensitive data such
        as passwords and keys removed, so that it can be safely logged.

        @type  app_config: ``dict``
        @param app_config: A dict containing the original, unprocessed version
                           of the app config. The app config is a merged dict
                           of database stored settings and user-entered
                           settings.

        :rtype: ``dict``
        :return: A ``dict` containing the launch configuration.
        """
        pass

    @abc.abstractmethod
    def provision_host(self, provider, task, name, cloud_config, app_config,
                       user_data):
        """
        Provision a host machine on the target infrastructure.

        This operation is designed to be a Celery task, and thus, can contain
        long-running operations.

        @type  provider: :class:`CloudBridge.CloudProvider`
        @param provider: Cloud provider where the supplied deployment is to be
                         created.

        @type  task: :class:`Task`
        @param task: A Task object, which can be used to report progress. See
                     ``tasks.Task`` for the interface details and sample
                     implementation.

        @type  name: ``str``
        @param name: Name of this deployment.

        @type  cloud_config: ``dict``
        @param cloud_config: A dict containing cloud infrastructure specific
                             configuration for this app.

        @type  app_config: ``dict``
        @param app_config: A dict containing the original, unprocessed version
                           of the app config. The app config is a merged dict
                           of database stored settings and user-entered
                           settings.

        @type  user_data: ``object``
        @param user_data: An object returned by the ``process_app_config()``
                          method which contains a validated and processed
                          version of the ``app_config``.

        :rtype: ``dict``
        :return: Results of the provisioning process. This dict must contain at
                 least the following keys:
                    * ``cloudLaunch``: Results of the CloudLaunch provisioning
                                       process
                    * ``host``: A dictionary with info about the provisioned
                                host. This dict must have at least the
                                following keys:
                        * ``address``: Host IP address or hostname
                        * ``pk``: Private portion of an SSH key for accessing
                                  the host
                        * ``user``: Username with which to access the host
        """
        pass

    @abc.abstractmethod
    def configure_host(self, host_config, app_config):
        """
        Configure the host for use by the appliance.

        @type  host_config: ``dict``
        @param host_config: A dict containing info about the host being
                            configured. For base implementation, it should have
                            at leasst the following keys:
                              * ``address``: Hostname or IP address of the host
                                             to configure.
                              * ``pk``: Private portion of an SSH key for
                                        accessing the host
                              * ``user``: Username with which to access the host

        @type  app_config: ``dict``
        @param app_config: A dict containing the original, unprocessed version
                            of the app config. The app config is a merged dict
                            of database stored settings and user-entered
                            settings.

        :rtype: ``dict``
        :return: Results of the configuring process.
        """
        pass

    @abc.abstractmethod
    def health_check(self, provider, deployment):
        """
        Check the health of this app.

        At a minimum, this will check the status of the VM on which the
        deployment is running. Applications can implement more elaborate
        health checks.

        @type  provider: :class:`CloudBridge.CloudProvider`
        @param provider: Cloud provider where the supplied deployment was
                         created.

        @type  deployment: ``dict``
        @param deployment: A dictionary describing an instance of the
                           app deployment. The dict must have at least
                           `launch_result` and `launch_status` keys.

        :rtype: ``dict``
        :return: A dictionary with possibly app-specific fields capturing
                 app health. At a minimum, ``instance_status`` field will be
                 available. If the deployment instance is not found by the
                 provider, the default return value is ``deleted`` for the
                 ``instance_status`` key.
        """
        pass

    @abc.abstractmethod
    def restart(self, provider, deployment):
        """
        Restart the appliance associated with the supplied deployment.

        This can simply restart the virtual machine on which the deployment
        is running or issue an app-specific call to perform the restart.

        @type  provider: :class:`CloudBridge.CloudProvider`
        @param provider: Cloud provider where the supplied deployment was
                         created.

        @type  deployment: ``dict``
        @param deployment: A dictionary describing an instance of the
                           app deployment to be restarted. The dict must have
                           at least `launch_result` and `launch_status` keys.

        :rtype: ``bool``
        :return: The result of restart invocation.
        """
        pass

    @abc.abstractmethod
    def delete(self, provider, deployment):
        """
        Delete resource(s) associated with the supplied deployment.

        *Note* that this method will delete resource(s) associated with
        the deployment - this is an un-recoverable action.

        @type  provider: :class:`CloudBridge.CloudProvider`
        @param provider: Cloud provider where the supplied deployment was
                         created.

        @type  deployment: ``dict``
        @param deployment: A dictionary describing an instance of the
                           app deployment to be deleted. The dict must have at
                           least `launch_result` and `launch_status` keys.

        :rtype: ``bool``
        :return: The result of delete invocation.
        """
        pass
