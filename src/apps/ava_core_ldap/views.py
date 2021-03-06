from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView

from apps.ava_core_ldap.models import ActiveDirectoryUser, ActiveDirectoryGroup, LDAPConfiguration, ActiveDirectoryHelper
from apps.ava_core_ldap.forms import  LDAPConfigurationForm


class LDAPConfigurationIndex(ListView):
    template_name = 'ldap/LDAPConfiguration_index.html'
    context_object_name = 'ldap_configuration_list'

    def get_queryset(self):
        return LDAPConfiguration.objects.all()

class LDAPConfigurationDetail(DetailView):
    model = LDAPConfiguration
    context_object_name = 'ldap_configuration'
    template_name = 'ldap/LDAPConfiguration_detail.html'

class LDAPConfigurationCreate(CreateView):
    model = LDAPConfiguration
    template_name = 'ldap/LDAPConfiguration.html'
    form_class = LDAPConfigurationForm

class LDAPConfigurationUpdate(UpdateView):
    model = LDAPConfiguration
    template_name = 'ldap/LDAPConfiguration.html'
    form_class = LDAPConfigurationForm

class LDAPConfigurationDelete(DeleteView):
    model = LDAPConfiguration
    template_name = 'confirm_delete.html'
    success_url = '/ldap/'

class ActiveDirectoryUserIndex(ListView):
    model = ActiveDirectoryUser
    template_name = 'ldap/ActiveDirectoryUser_index.html'

    def get_context_data(self, **kwargs):
        context = super(ActiveDirectoryUserIndex, self).get_context_data(**kwargs)
        config_pk = self.kwargs.get('pk')
        if config_pk:
            instance = get_object_or_404(LDAPConfiguration, pk=config_pk)
            context['ldap_user_list'] = ActiveDirectoryUser.objects.filter(ldap_configuration=instance)
            context['ldap_configuration'] = instance
        return context

class ActiveDirectoryUserDetail(DetailView):
    model = ActiveDirectoryUser
    context_object_name = 'activedirectoryuser'
    template_name = 'ldap/ActiveDirectoryUser_detail.html'

class ActiveDirectoryUserCreate(CreateView):
    model = ActiveDirectoryUser
    template_name = 'ldap/ActiveDirectoryUser.html'
    form_class = LDAPConfigurationForm

class ActiveDirectoryUserUpdate(UpdateView):
    model = ActiveDirectoryUser
    template_name = 'ldap/ActiveDirectoryUser.html'
    form_class = LDAPConfigurationForm

class ActiveDirectoryUserDelete(DeleteView):
    model = ActiveDirectoryUser
    template_name = 'confirm_delete.html'
    success_url = '/ldap/'

class ActiveDirectoryGroupIndex(ListView):
    model = ActiveDirectoryGroup
    template_name = 'ldap/ActiveDirectoryGroup_index.html'

    def get_context_data(self, **kwargs):
        context = super(ActiveDirectoryGroupIndex, self).get_context_data(**kwargs)
        config_pk = self.kwargs.get('pk')
        if config_pk:
            instance = get_object_or_404(LDAPConfiguration, pk=config_pk)
            context['ldap_group_list'] = ActiveDirectoryGroup.objects.filter(ldap_configuration=instance)
            context['ldap_configuration'] = instance
        return context

class ActiveDirectoryGroupDetail(DetailView):
    model = ActiveDirectoryGroup
    context_object_name = 'activedirectorygroup'
    template_name = 'ldap/ActiveDirectoryGroup_detail.html'

class ActiveDirectoryGroupCreate(CreateView):
    model = ActiveDirectoryGroup
    template_name = 'ldap/ActiveDirectoryGroup.html'
    form_class = LDAPConfigurationForm

class ActiveDirectoryGroupUpdate(UpdateView):
        model = ActiveDirectoryGroup
        template_name = 'ldap/ActiveDirectoryGroup.html'
        form_class = LDAPConfigurationForm

class ActiveDirectoryGroupDelete(DeleteView):
        model = ActiveDirectoryGroup
        template_name = 'confirm_delete.html'
        success_url = '/ldap/'

class LDAPConfigurationGetUsers(ListView):
    model = ActiveDirectoryUser
    context_object_name = 'activedirectoryuser_list'
    template_name = 'ldap/ActiveDirectoryUser_index.html'

    def get_context_data(self, **kwargs):
        self.get_users()
        context = super(LDAPConfigurationGetUsers, self).get_context_data(**kwargs)
        config_pk = self.kwargs.get('pk')
        if config_pk:
            instance = get_object_or_404(LDAPConfiguration, pk=config_pk)
            context['activedirectoryuser_list'] = ActiveDirectoryUser.objects.filter(ldap_configuration=instance)
        return context

    def get_users(self):
        config_pk = self.kwargs.get('pk')
        if config_pk:
            instance = get_object_or_404(LDAPConfiguration, pk=config_pk)
            adHelper = ActiveDirectoryHelper()
            adHelper.getUsers(instance)

        return True



# class LDAPConfigurationGetAll(ListView):
#     model = ActiveDirectoryUser
#     template_name = 'ldap/items.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(LDAPConfigurationGetAll, self).get_context_data(**kwargs)
#         config_pk = self.kwargs.get('pk')
#         if config_pk:
#             instance = get_object_or_404(LDAPConfiguration, pk=config_pk)
#             adHelper = ActiveDirectoryHelper()
#             adHelper.getUsers(instance)
#             adHelper.getGroups(instance)
#             adHelper.getUsers(instance)
#
#         context['item_type'] = 'user'
#         ad_groups = ActiveDirectoryGroup.objects.filter(ldapConfiguration=instance)
#
#         for adg in ad_groups:
#             try:
#                 org_g = OrganisationGroup.objects.get(name=adg.cn)
#                 groups = adg.member.all()
#                 for g in groups:
#                     try:
#                         user = Identifier.objects.get(identifier=g.sAMAccountName,identifiertype=Identifier.UNAME)
#                         GroupIdentifier.objects.get_or_create(identifier=user, group=org_g)
#                         user1 = Identifier.objects.get(identifier=g.sAMAccountName+"@avasecure.com",identifiertype=Identifier.EMAIL)
#                         GroupIdentifier.objects.get_or_create(identifier=user1, group=org_g)
#                     except Identifier.DoesNotExist:
#                         print " No such id :: " + g.sAMAccountName
#
#
#             except OrganisationGroup.DoesNotExist:
#                 print "No such group :: " + adg.cn
#
#         context['ldap_item_list'] = ActiveDirectoryUser.objects.filter(ldapConfiguration=instance)
#         return context

class LDAPConfigurationGetGroups(ListView):
    model = ActiveDirectoryGroup
    context_object_name = 'activedirectorygroup_list'
    template_name = 'ldap/ActiveDirectoryGroup_index.html'

    def get_context_data(self, **kwargs):
        self.get_groups()
        context = super(LDAPConfigurationGetGroups, self).get_context_data(**kwargs)
        config_pk = self.kwargs.get('pk')
        if config_pk:
            instance = get_object_or_404(LDAPConfiguration, pk=config_pk)
            #context['ldap_configuration'] = instance
            context['activedirectorygroup_list'] = ActiveDirectoryGroup.objects.filter(ldap_configuration=instance)
        return context

    def get_groups(self):
        config_pk = self.kwargs.get('pk')
        if config_pk:
            instance = get_object_or_404(LDAPConfiguration, pk=config_pk)
            adHelper = ActiveDirectoryHelper()
            adHelper.getGroups(instance)




    #def populate_groups(self):
        # context['item_type'] = 'user'
        # ad_groups = ActiveDirectoryGroup.objects.filter(ldapConfiguration=instance)
        #
        # for adg in ad_groups:
        #     try:
        #         org_g = OrganisationGroup.objects.get(name=adg.cn)
        #         groups = adg.member.all()
        #         for g in groups:
        #             try:
        #                 user = Identifier.objects.get(identifier=g.sAMAccountName,identifiertype=Identifier.UNAME)
        #                 GroupIdentifier.objects.get_or_create(identifier=user, group=org_g)
        #                 user1 = Identifier.objects.get(identifier=g.sAMAccountName+"@avasecure.com",identifiertype=Identifier.EMAIL)
        #                 GroupIdentifier.objects.get_or_create(identifier=user1, group=org_g)
        #             except Identifier.DoesNotExist:
        #                 print " No such id :: " + g.sAMAccountName
        #
        #
        #     except OrganisationGroup.DoesNotExist:
        #         print "No such group :: " + adg.cn



