from odoo.tests import TransactionCase, new_test_user, tagged


@tagged('post_install', '-at_install')
class TestPricelistAccess(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        own = 'base.group_user,restrict_pricelist_users.group_view_own_pricelists'
        cls.user_1 = new_test_user(cls.env, login='rpu_u1', groups=own)
        cls.user_2 = new_test_user(cls.env, login='rpu_u2', groups=own)
        cls.user_all = new_test_user(
            cls.env, login='rpu_all',
            groups='base.group_user,restrict_pricelist_users.group_view_all_pricelists',
        )
        cls.user_plain = new_test_user(cls.env, login='rpu_plain', groups='base.group_user')

        Pricelist = cls.env['product.pricelist']
        cls.pl_1 = Pricelist.create({'name': 'RPU PL1', 'allowed_users': [(6, 0, cls.user_1.ids)]})
        cls.pl_public = Pricelist.create({'name': 'RPU PL2'})
        cls.test_pricelists = cls.pl_1 | cls.pl_public

    def _visible(self, user):
        return self.env['product.pricelist'].with_user(user).search(
            [('id', 'in', self.test_pricelists.ids)])

    def test_allowed_user_sees_own_and_public(self):
        self.assertEqual(self._visible(self.user_1), self.pl_1 | self.pl_public)

    def test_other_user_sees_only_public(self):
        self.assertEqual(self._visible(self.user_2), self.pl_public)
        self.assertFalse(self.pl_1.with_user(self.user_2).has_access('read'))

    def test_all_pricelists_group_sees_everything(self):
        self.assertTrue(self.user_all.has_group('restrict_pricelist_users.group_view_own_pricelists'))
        self.assertEqual(self._visible(self.user_all), self.test_pricelists)

    def test_user_without_groups_is_not_restricted(self):
        self.assertEqual(self._visible(self.user_plain), self.test_pricelists)

    def test_group_change_applies_immediately(self):
        self.assertEqual(self._visible(self.user_2), self.pl_public)
        self.user_2.group_ids = [(4, self.env.ref('restrict_pricelist_users.group_view_all_pricelists').id)]
        self.assertEqual(self._visible(self.user_2), self.test_pricelists)
