# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import *
import datetime
import time
import logging
import random

# 一般人基本檔 團員 會員 收費員 顧問
_logger = logging.getLogger(__name__)

class NormalP(models.Model):
    # 捐款人
    _name = 'normal.p'
    _order = 'sequence,new_coding'
    _description = u'捐款者基本資料管理'

    new_coding = fields.Char(string='捐款者編號')
    temp_new_coding = fields.Char(string='暫存捐款者編號')
    # old_coding = fields.Char(string='舊捐款者編號')
    special_tag = fields.Boolean(string='眷屬檔沒有的團員')
    w_id = fields.Char(string='舊團員編號')
    number = fields.Char(string='序號')
    name = fields.Char(string='姓名',required = True)
    birth = fields.Date(string='生日')
    cellphone = fields.Char(string='手機')
    con_phone = fields.Char(string='連絡電話')
    con_phone2 = fields.Char(string='連絡電話(二)')
    zip = fields.Char(string='收據郵遞區號')
    rec_addr = fields.Char(string='收據寄送地址')
    zip_code = fields.Char(string='報表郵遞區號')
    con_addr = fields.Char(string='報表寄送地址')
    old_rec_addr = fields.Char(string='原收據寄送地址', readonly=True) # 因縣市合併的關係, 備份收據寄送地址修正前的地址
    old_con_addr = fields.Char(string='原報表寄送地址', readonly=True) # 因縣市合併的關係, 備份報表寄送地址修正前的地址

    # 信用卡捐款相關欄位

    credit_parent = fields.Many2one(comodel_name='normal.p',string='信用卡持卡人')
    credit_family = fields.One2many(comodel_name='normal.p',inverse_name='credit_parent',string='信用卡眷屬')

    credit_family_number = fields.Integer(string = '信用卡扣款人數', compute='compute_credit_donate_total')
    credit_is_donate = fields.Boolean('是否捐助', default = True)
    credit_money = fields.Integer('信用卡總額')
    credit_zip = fields.Char('信用卡郵遞區號')
    credit_addr = fields.Char('信用卡收據地址')
    debit_method = fields.Selection(selection=[(1, '5日扣款'), (2, '20日扣款'), (3, '季日扣款'), (4, '年繳扣款'), (5, '單次扣款')],
                                    string='信用卡扣款方式')
    is_donated_credit = fields.Boolean('是否捐款(收件人)')
    is_sent = fields.Boolean('每次寄送收據')
    year_sent = fields.Boolean('年底一次開立')
    no_need = fields.Boolean('不需收據')
    credit_bridge_money = fields.Integer('A.造橋')
    credit_road_money = fields.Integer('B.補路')
    credit_coffin_money = fields.Integer('C.施棺')
    credit_poor_money = fields.Integer('D.貧困扶助')
    credit_normal_money = fields.Integer('E.一般捐款')
    credit_total_money = fields.Integer('信用卡個人捐款總額')
    credit_donate_total = fields.Integer('信用卡捐款總額', compute='compute_credit_donate_total')
    credit_family_list = fields.Char(string='信用卡捐款人列表', compute='compute_family_list')
    credit_number = fields.Char('信用卡卡號末四碼')
    credit_bank = fields.Char('發卡銀行')

    cashier_name_credit = fields.Many2one(comodel_name='cashier.base', string='收費員姓名', ondelete='cascade', index=True)
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', ondelete='cascade')
    temp_key_in_user = fields.Char(string='輸入人員_temp')
    db_chang_date = fields.Date(string='異動日期')
    build_date = fields.Date(string='建檔日期', default=fields.Date.today)

    email = fields.Char(string='Email')
    type = fields.Many2many(comodel_name='people.type', string='人員種類')
    self_iden = fields.Char(string='身分證字號')

    come_date = fields.Date(string='到職日期')
    lev_date = fields.Date(string='離職日期')
    ps = fields.Text(string='備註')
    habbit_donate = fields.Selection(selection=[(01, '造橋'), (02, '補路'), (03, '施棺'), (04, '伙食費'), (05, '貧困扶助'),(06, '一般捐款'), (99, '其他工程')],
                                     string='喜好捐款')
    cashier_name = fields.Many2one(comodel_name='cashier.base', string='收費員姓名', ondelete='cascade', index = True)
    temp_cashier_name = fields.Char(string='收費員姓名_temp')
    donate_cycle = fields.Selection(selection=[('03', '季繳'), ('06', '半年繳'), ('12', '年繳')], string='捐助週期')
    rec_type = fields.Selection(selection=[(1, '正常'), (2, '年收據')], string='收據狀態')
    rec_send = fields.Boolean(string='收據寄送', default=True)

    self = fields.Char(string='自訂排序')
    report_send = fields.Boolean(string='報表寄送', default = True)
    thanks_send = fields.Boolean(string='感謝狀寄送')
    prints = fields.Boolean(string='是否列印')
    prints_id = fields.Char(string='核印批號')
    prints_date = fields.Char(string='核印日期')
    bank_id = fields.Char(string='扣款銀行代碼')
    bank = fields.Char(string='扣款銀行')
    bank_id2 = fields.Char(string='扣款分行代碼')
    bank2 = fields.Char(string='扣款分行')
    account = fields.Char(string='銀行帳號')
    bank_check = fields.Boolean(string='銀行核印')
    ps2 = fields.Text(string='備註')

    comp_id = fields.Char(string='電腦編號')
    member_list = fields.Char(string='會員名冊編號')
    year = fields.Char(string='繳費年度')
    should_pay = fields.Integer(string='應繳金額')
    cashier = fields.Many2one(comodel_name='cashier.base', string='收費員')
    temp_cashier = fields.Char(string='收費員_temp')
    pay_date = fields.Date(string='收費日期')
    booklist = fields.Boolean(string='名冊列印', default=True)
    member_type = fields.Selection(selection=[(1, '基本會員'), (2, '贊助會員')], string='會員種類')
    hire_date = fields.Date(string='雇用日期')
    merge_report = fields.Boolean(string='年收據寄送', help='將捐款者的收據整合進該住址') # help 可以在開發者模式下的欄位看到內容
    #團員檔及團員眷屬檔設定戶長之功能
    parent = fields.Many2one(comodel_name='normal.p', string='戶長', ondelete='cascade', index = True)
    donate_family1 = fields.One2many(comodel_name='normal.p', inverse_name='parent', string='團員眷屬')
    # 來判斷你是不是老大
    member_data_ids = fields.Many2one(comodel_name='member.data', string='關聯的顧問會員檔')
    donate_history_ids = fields.One2many(comodel_name='donate.order', inverse_name='donate_member')
    donate_single_history_ids = fields.One2many(comodel_name='donate.single', inverse_name='donate_member')
    #會員收費檔及顧問檔收費檔關聯
    member_pay_history = fields.One2many(comodel_name='associatemember.fee', inverse_name='normal_p_id')
    consultant_pay_history = fields.One2many(comodel_name='consultant.fee', inverse_name='normal_p_id')
    member_id = fields.Char(string='會員編號')
    consultant_id = fields.Char(string='顧問編號')

    sequence = fields.Integer(string='排序',default=1)
    member_sequence = fields.Char(string='會員排序')

    is_donate = fields.Boolean(string='是否捐助', default=True)
    is_merge = fields.Boolean(string='是否合併收據', default=True)

    donate_family_list = fields.Char(string='眷屬列表', compute='compute_faamily_list')
    active = fields.Boolean(default=True)
    is_same_addr = fields.Boolean(string='報表地址同收據地址')
    auto_num = fields.Char('自動地區編號')
    check_donate_order = fields.Boolean(string='捐款紀錄查詢', default = False)
    is_delete = fields.Boolean(string='未有捐款紀錄', default = False)

    last_donate_date = fields.Date('上次捐款日期')
    last_member_payment_date = fields.Date('上次會員繳費日期')
    last_consultant_payment_date = fields.Date('上次顧問繳費日期')
    last_donate_type = fields.Selection(selection=[(01, '造橋'), (02, '補路'), (03, '施棺'), (05, '貧困扶助'),(06, '一般捐款')],string='捐款種類')
    last_donate_money = fields.Integer('上次捐款金額')
    donate_batch_setting = fields.Boolean(string='確認捐款', default = False)
    postal_code_id = fields.Many2one(comodel_name='postal.code', string='郵遞區號關聯')
    print_all_donor_list = fields.Boolean(string='列印願意捐助的眷屬')
    head_of_household = fields.Integer(string='我是戶長')

    donor = fields.Many2one(comodel_name='res.users', string="捐款登入者")

    old_coffin_donation = fields.One2many(comodel_name='old.coffin.donation', inverse_name='normal_p_id') # 系統上線前, 紀錄舊系統施棺捐助情況
    coffin_donation = fields.One2many(comodel_name='coffin.donation', inverse_name='normal_p_id') # 系統上線後, 紀錄系統的施棺捐助情況
    donor_sign_in = fields.Boolean(string='核准捐款者登入', default = False)
    initial_password = fields.Char('初始密碼', readonly=True)

    @api.depends('credit_family.credit_is_donate')
    def compute_credit_donate_total(self):
        for line in self:
            line.credit_donate_total = 0
            if line.credit_family:
                total = 0
                number = 0
                for row in line.credit_family:
                    number = number + 1
                    if row.credit_is_donate == True:
                        total = total + row.credit_total_money
                line.credit_family_number = number
                line.credit_donate_total = line.credit_donate_total + total
            else:
                line.credit_donate_total = 0

    @api.onchange('debit_method')
    def check_credit_debit_method(self):
        if self.credit_family:
            for line in self.credit_family:
                line.debit_method = self.debit_method

    @api.multi
    def write(self,vals): # 信用卡扣款功能的防呆機制, 覆寫odoo原本的write()
      res_id = super(NormalP,self).write(vals)
      if self.credit_parent:
          if self.debit_method is False:
              raise ValidationError(u'捐款者編號:%s， 請選擇扣款方式' % self.new_coding)
          if self.is_sent is False and self.year_sent is False:
              raise ValidationError(u'捐款者編號:%s，信用卡收據寄送方式請至少選擇一種' % self.new_coding)
          if self.is_sent is True and self.year_sent is True:
              raise ValidationError(u'捐款者編號:%s，信用卡收據寄送方式只能選擇一種' % self.new_coding)
      return res_id

    @api.onchange('is_donated_credit')
    def check_credit_recipient(self):
        i = 0
        if self.credit_parent:
            for line in self.credit_parent.credit_family:
                if line.is_donated_credit == True:
                    i = i + 1
            if i > 1:
                raise ValidationError(u'捐款者編號:%s  %s的信用卡捐款收據收件人只能有一位' % (self.credit_parent.new_coding, self.credit_parent.name))

    # 設定上一筆捐款 如果捐款種類有選擇, 則自動帶入捐款金額100元
    @api.onchange('last_donate_type')
    def set_default_last_donate_money(self):
        if self.last_donate_type != False and self.last_donate_money == 0:
            self.last_donate_money = 100

    @api.onchange('credit_bridge_money', 'credit_road_money', 'credit_coffin_money', 'credit_poor_money','credit_normal_money')
    def compute_donate_total(self):
        self.credit_total_money = 0
        self.credit_total_money = self.credit_bridge_money + self.credit_road_money + self.credit_coffin_money + self.credit_poor_money + self.credit_normal_money

    @api.onchange('credit_parent') #one2many的credit_family也要帶入
    def set_credit_data(self):
        if self.credit_parent != False:
            data = self.env['normal.p'].search([('id','=',self.credit_parent.ids)])
            self.credit_zip = data.credit_zip
            self.credit_addr = data.credit_addr
            self.credit_number = data.credit_number
            self.debit_method = data.debit_method
            self.is_sent = data.is_sent
            self.credit_bank = data.credit_bank
            self.year_sent = data.year_sent
            self.no_need = data.no_need

    @api.onchange('check_donate_order')
    def check_unlink(self):
        if self.check_donate_order:
            for line in self.donate_family1:
                if (len(line.donate_history_ids) != 0 or len(line.donate_single_history_ids) != 0 ) is True:
                    line.is_delete = False
                elif (len(line.donate_history_ids) == 0 and len(line.donate_single_history_ids) == 0) is True:
                    line.is_delete = True

    # 合併捐款者功能
    def action_chang_donater_wizard(self):
        wizard_data = self.env['chang.donater'].create({
            'from_target': self.id
        })
        action = self.env.ref('cdg_base.chang_donater_action').read()[0]
        action['res_id'] = wizard_data.id
        return action

    # 批次更改捐款檔的收件人和地址
    def action_donate_single_trans(self):
        donor_data = self.env['donate.single.trans'].create({
            'normal_p_code': self.id
        })
        action = self.env.ref('cdg_base.action_donate_single_trans').read()[0]
        action['res_id'] = donor_data.id
        return action

    #批次更改戶長
    def action_parent_trans(self):
       parent_data = self.env['wizard.parent.trans'].create({
           'normal_p_code':self.id
       })
       action = self.env.ref('cdg_base.action_wizard_parent_trans').read()[0]
       action['res_id'] = parent_data.id
       return action

    #清空信用卡的資料
    def clear_credit_data(self):
        if self.credit_parent and self.credit_family:
            for line in self.credit_family:
                line.credit_parent = None
                line.credit_bank = ""
                line.is_donated_credit = False
                line.credit_number = ""
                line.credit_money = 0
                line.debit_method = False
                line.credit_zip = ""
                line.credit_addr = ""
                line.credit_normal_money = 0
                line.credit_poor_money = 0
                line.credit_coffin_money = 0
                line.credit_road_money = 0
                line.credit_bridge_money = 0
                line.credit_total_money = 0
                line.is_sent = False
                line.year_sent = False
                line.no_need = False
        elif (self.credit_parent and len(self.credit_family) == 0) or self.name != self.credit_parent.name:
            raise ValidationError(u'捐款者編號:%s  %s 並非信用卡持卡人，無法清空信用卡扣款資料' % (self.new_coding, self.name))

    # 核准捐款者登入系統查詢自己的捐款紀錄, 並亂數產生登入密碼
    def create_donor_account(self):
        auth = ''
        for i in range(0, 2):
            current_code = random.randint(65, 90)
            auth += chr(current_code) # 大寫英文的 ASCII 轉換成英文字母, 所以這部份需要用 char 的轉型方法
        for i in range(0, 6):
            current_code = random.randint(0, 9)
            auth += str(current_code)
        self.initial_password = auth
        res_id = self.env['res.users'].create({
            'login': self.new_coding,
            'password': self.initial_password,
            'name': self.name,
            'sel_groups_15':15,
            'sel_groups_32_33': False,
        })
        self.donor = res_id.id
        self.donor_sign_in = True
        return True

    def start_donate(self):
        action = self.env.ref('cdg_base.start_donate_action').read()[0]
        user = self.env['res.users'].search([('login', '=', self.env.user.login)])
        action['context'] = {'default_donate_member':self.id, 'default_payment_method':user.payment_method}
        return action

    def historypersonal(self):
        action = self.env.ref('cdg_base.donate_single_view_action').read()[0]
        action['context'] ={} # remove default domain condition in search box
        action['domain'] =[] # remove any value in search box
        action['domain'] = ['&',('donate_member', '=', self.id),('state','!=',3)]  # set new domain condition to search data
        return action

    def cashier_block(self, ids):
        res = []
        for line in ids:
            res.append([4,line])
            wizard_data = self.env['cashier.block'].create({'from_target': res})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cashier.block',
            'name': '收費員捐款者名冊-新',
            'view_mode': 'form',
            'res_id': wizard_data.id,
            'target': 'new',
        }

    def cashier_member(self, ids):
        res = []
        for line in ids:
            res.append([4,line])
            wizard_data = self.env['cashier.member'].create({'from_target': res})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cashier.member',
            'name': '收費員會員名冊-新',
            'view_mode': 'form',
            'res_id': wizard_data.id,
            'target': 'new',
        }

    def cashier_consultant(self, ids):
        res = []
        for line in ids:
            res.append([4,line])
            wizard_data = self.env['cashier.consultant'].create({'from_target': res})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cashier.consultant',
            'name': '收費員顧問名冊-新',
            'view_mode': 'form',
            'res_id': wizard_data.id,
            'target': 'new',
        }

    def donate_batch(self,ids):
        res = []
        for line in ids:
            res.append([4, line])
        wizard_data = self.env['wizard.batch'].create({
            'donate_line': res
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.batch',
            'name': '批次捐款項目',
            'view_mode': 'form',
            'res_id': wizard_data.id,
            'target': 'new',
        }

    def cashier_transfer_batch(self,ids):
        res = []
        docs = self.env['normal.p'].browse(ids)
        cashier_name = 0
        for line in docs:
            if cashier_name == 0:
                cashier_name = line.cashier_name.id
            elif cashier_name != line.cashier_name.id:
                raise ValidationError(u'新捐款者編號: %s 的收費員是%s, 與原收費員不同, 因此無法合併' % (line.new_coding, line.cashier_name.name))

        for line in ids:
            res.append([4, line])
        wizard_data = self.env['cashier.transfer'].create({
            'new_cashier': cashier_name,
            'old_cashier': cashier_name,
            'from_target': res
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cashier.transfer',
            'name': '收費員捐款者合併',
            'view_mode': 'form',
            'res_id': wizard_data.id,
            'target': 'new',
        }

    def credit_batch(self, ids):
        res = []
        for line in ids:
            res.append([4, line])
        wizard_data = self.env['wizard.credit.batch'].create({
            'donate_line': res
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.credit.batch',
            'name': '信用卡批次捐款',
            'view_mode': 'form',
            'res_id': wizard_data.id,
            'target': 'new',
        }

    def check_batch_donate(self):
        if self.donate_batch_setting == True:
            self.donate_batch_setting = False
        elif self.donate_batch_setting == False:
            self.donate_batch_setting = True
        return True

    @api.depends('donate_family1.is_donate','donate_family1.is_merge')
    def compute_faamily_list(self):
        for line in self:
            sb = ''
            str = ''
            donate_type = ''
            for row in line.donate_family1:
                if row.last_donate_type == 1:
                    donate_type =  u'造橋'
                if row.last_donate_type == 2:
                    donate_type = u'補路'
                if row.last_donate_type == 3:
                    donate_type = u'施棺'
                if row.last_donate_type == 4:
                    donate_type = u'伙食費'
                if row.last_donate_type == 5:
                    donate_type = u'貧困扶助'
                if row.last_donate_type == 6:
                    donate_type = u'一般捐款'
                if row.last_donate_type == 99:
                    donate_type = u'其他工程'
                if row.last_donate_type == False:
                    donate_type = ''

                if row.is_donate is False:
                    str += u'(X %s %s %s),' % (row.name , donate_type , row.last_donate_money)
                elif row.is_merge is False:
                    sb += u'(★ %s %s %s),' % (row.name , donate_type , row.last_donate_money)
                else:
                    sb += u'(%s %s %s),' % (row.name , donate_type , row.last_donate_money)
            if str != '':
                str = str.rstrip(',')
            if str == '':
                sb = sb.rstrip(',')
            line.donate_family_list = sb+str

    def compute_family_list(self):
        for line in self:
            family_list = list()
            temp_list = []
            for row in line.credit_family:
                if row.credit_is_donate == True:
                    if row.credit_bridge_money != 0:
                        family_list.append('('+row.name+ u' 造橋 '+str(row.credit_bridge_money) +')')
                    if row.credit_road_money != 0:
                        family_list.append('(' + row.name + u' 補路 ' + str(row.credit_road_money) + ')')
                    if row.credit_coffin_money != 0:
                        family_list.append('(' + row.name + u' 施棺 ' + str(row.credit_coffin_money) + ')')
                    if row.credit_poor_money != 0:
                        family_list.append('(' + row.name + u' 貧困扶助 ' + str(row.credit_poor_money) + ')')
                    if row.credit_normal_money != 0:
                        family_list.append('(' + row.name + u' 一般捐款 ' + str(row.credit_normal_money) + ')')
                    if row.credit_bridge_money == 0 and row.credit_road_money == 0 and row.credit_coffin_money == 0 and row.credit_poor_money == 0 and row.credit_normal_money == 0:
                        family_list.append('(X' + row.name + ')')
                else:
                    if row.credit_bridge_money != 0:
                        family_list.append('(X' + row.name + u' 造橋 ' + str(row.credit_bridge_money) + ')')
                    if row.credit_road_money != 0:
                        family_list.append('(X' + row.name + u' 補路 ' + str(row.credit_road_money) + ')')
                    if row.credit_coffin_money != 0:
                        family_list.append('(X' + row.name + u' 施棺 ' + str(row.credit_coffin_money) + ')')
                    if row.credit_poor_money != 0:
                        family_list.append('(X' + row.name + u' 貧困扶助 ' + str(row.credit_poor_money) + ')')
                    if row.credit_normal_money != 0:
                        family_list.append('(X' + row.name + u' 一般捐款 ' + str(row.credit_normal_money) + ')')
                    if row.credit_bridge_money == 0 and row.credit_road_money == 0 and row.credit_coffin_money == 0 and row.credit_poor_money == 0 and row.credit_normal_money == 0:
                        family_list.append('(X' + row.name + ')')
                line.credit_family_list = ','.join(family_list)
            if line.credit_family_list:
                temp_list = line.credit_family_list.split(',')
                is_donate =''
                not_donate =''
                for row in temp_list:
                    if '(X' in row:
                        not_donate = not_donate + row + ','
                    else:
                        is_donate = is_donate + row + ','
                if not_donate == '':
                    line.credit_family_list = is_donate.rstrip(',')
                elif not_donate != '':
                    line.credit_family_list = is_donate + not_donate.rstrip(',')

    def toggle_credit_donate_receipt(self):
        self.is_donated_credit = not self.is_donated_credit

    def toggle_credit_donate(self):
        self.credit_is_donate = not self.credit_is_donate

    def toggle_donate(self):
        self.is_donate = not self.is_donate

    def toggle_merge(self):
        self.is_merge = not self.is_merge

    def toggle_recsend(self):
        self.rec_send = not self.rec_send

    def toggle_reportsend(self):
        self.report_send = not self.report_send

    def all_addr_chnage(self):
        for line in self.donate_family1:
            if line:
                line.zip = self.zip
                line.rec_addr = self.rec_addr
                line.zip_code = self.zip_code
                line.con_addr = self.con_addr
            else:
                break

    def combine_addr(self):
        for line in self.donate_family1:
            if line:
                if line.is_merge is True:
                    line.zip = self.zip
                    line.rec_addr =  self.rec_addr
                    line.zip_code = self.zip_code
                    line.con_addr = self.con_addr
            else:
                break

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if u'\u4e00' <= name <=u'\u9fff':
            domain = [('name', operator, name)]
        else:
            domain = ['|', ('w_id', operator, name), ('new_coding', operator, name)]

        banks = self.search(domain + args, limit=limit)
        return banks.name_get()

    @api.multi
    def my_self(self):
        return [('parent', '=', self.id)]

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "{%s} %s {%s}" % (record.new_coding, record.name,record.w_id)
            result.append((record.id, name))
        return result

    def check_type(self, line):
        if line.member_type.id > 0:
            return [(4, line.member_type.id)]
        else:
            return None

    @api.onchange('cashier_name')
    def setcashier(self):
        self.cashier = self.cashier_name.name


    @api.onchange('is_same_addr')
    def rec_addr_same_con_addr(self):
        if self.is_same_addr is True:
            if not self.zip or not self.rec_addr:
                raise ValidationError(u'收據郵遞區號或收據寄送地址不能為空白')
            else:
                self.zip_code = self.zip
                self.con_addr = self.rec_addr

    def data_input_form_DB(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 團員眷屬檔')
        i = 1
        for line in lines:
            _logger.error(' %s / %s', i, len(lines))
            self.create({
                'w_id': line[u'團員編號'],
                'number': line[u'序號'],
                'name': line[u'姓名'],
                'cellphone': line[u'手機'],
                'con_addr': line[u'通訊地址'],
                'con_phone': line[u'電話一'],
                'con_phone2': line[u'電話二'],
                'zip_code': line[u'郵遞區號'],
                'type': 1,
                'habbit_donate': self.check_habbit(line[u'捐助種類編號']),
                'rec_send': self.checkbool(line[u'收據寄送']),
                'is_donate': self.checkbool(line[u'是否捐助']),
                'self': line[u'自訂排序'],
                'key_in_user': self.check_user(line[u'輸入人員']),
                'birth': self.check_db_date(line[u'建檔日期']),
                'db_chang_date': self.check(line[u'異動日期'])
            })
            i += 1

    def check_habbit(self, habbit):
        if habbit == u'01':
            return 01
        elif habbit == u'02':
            return 02
        elif habbit == u'03':
            return 03
        elif habbit == u'04':
            return 04
        elif habbit == u'05':
            return 05
        elif habbit == u'06':
            return 06
        elif habbit == u'99':
            return 99
        else:
            return None

    # 生日裡面有亂放東西，需要驗證是否真的是YYYY-MM-DD的格式
    def check_db_date(self, date):
        if date:
            try:
                time.strptime(date, "%Y-%m-%d")
                return date
            except:
                return None
        else:
            return None

    def check_user(self, row):
        check = self.env['c.worker'].search([('w_id', '=', row)])
        if check.id > 0:
            return check.id
        else:
            return False

    def set_parent(self):
        self.search([]).remove()

    @api.onchange('parent')
    def set_rec_zip(self):
        if self.parent:
            self.zip = self.parent.zip
            self.rec_addr = self.parent.rec_addr
            self.cashier_name = self.parent.cashier_name

    @api.onchange('zip','zip_code')
    def set_postal_code_id(self):
        flag = True
        if self.zip:
            for ch in self.zip:
                if not u'\u0030' <= ch <=u'\u0039':
                    raise ValidationError(u'收據郵遞區號輸入格式錯誤，請重新輸入')
                if int(self.zip[0]) == 0:
                    raise ValidationError(u'收據郵遞區號輸入格式錯誤，請重新輸入')

            if len(self.zip) < 3:
                raise ValidationError(u'收據郵遞區號為三碼，請重新輸入')
            else:
                for line in self.postal_code_id:
                    if self.zip == line.zip:
                        self.postal_code_id = line.id

        if self.zip_code:
            for ch in self.zip_code:
                if not u'\u0030' <= ch <= u'\u0039':
                    raise ValidationError(u'收據郵遞區號輸入格式錯誤，請重新輸入')
                if int(self.zip_code[0]) == 0:
                    raise ValidationError(u'收據郵遞區號輸入格式錯誤，請重新輸入')

            if len(self.zip_code) < 3:
                raise ValidationError(u'報表郵遞區號為三碼，請重新輸入')
            else:
                for line in self.postal_code_id:
                    if self.zip_code == line.zip:
                        self.postal_code_id = line.id

    # def set_parent(self):
    #     member = self.search([('w_id', '!=', None), ('number', '=', '1')])
    #     conn = psycopg2.connect("dbname=old_cdg user=odoo password=odoo")
    #     cur = conn.cursor()
    #     i = 1
    #     for line in member:
    #         # try:
    #         sql = "UPDATE normal_p SET parent = '{}' WHERE w_id = '{}' AND number != '1'".format(str(line.id),
    #                                                                                              str(line.w_id))
    #         _logger.error('it is run to %s line', i)
    #         cur.execute(sql)
    #         # except Exception:
    #         #     _logger.error('it is run to %s line', i)
    #         #     pass
    #         i += 1
    #     conn.commit()
    #     cur.close()
    #     conn.close()

    def data_input_from_database(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 團員檔')
        i = 1
        for line in lines:
            _logger.error(' %s / %s', i, len(lines))
            exist = False
            member = self.search([('w_id', '=', line[u'團員編號']), ('number', '=', '1'), ('name', '=', line[u'姓名'])])
            if member.id > 0:
                exist = True
            if exist is False and member.special_tag is not True:
                id_create = self.create({
                    'special_tag': True,
                    'w_id': line[u'團員編號'],
                    'number': u'0',
                    'name': line[u'姓名'],
                    'birth': self.check(line[u'出生日期']),
                    'cellphone': line[u'手機'],
                    'zip_code':line[u'郵遞區號'],
                    'con_addr': line[u'通訊地址'],
                    'con_phone': line[u'電話一'],
                    'con_phone2': line[u'電話二'],
                    'donate_cycle': line[u'捐助週期'],
                    'ps2': line[u'備註'],
                    'rec_send': self.checkbool(line[u'收據寄送']),
                    'bank_id': line[u'扣款銀行代碼'],
                    'bank_id2': line[u'扣款分行代碼'],
                    'thanks_send': self.checkbool(line[u'感謝狀寄送']),
                    'report_send': self.checkbool(line[u'報表寄送']),
                    'bank_check': self.checkbool(line[u'銀行核印']),
                    'cashier': line[u'收費員編號'],
                    'build_date': self.check_db_date(line[u'建檔日期']),
                    'db_chang_date': self.check(line[u'異動日期']),
                    'key_in_user': self.check_user(line[u'輸入人員']),
                })

            i += 1

    def check(self, date_check):
        if date_check:
            return date_check
        else:
            return None

    def checkbool(self, bool):
        if bool == 'Y':
            return True
        elif bool == 'N':
            return False

    # @api.onchange('zip', 'type')
    # def rec_addr_change(self):
    #     if self.name:
    #         self.old_coding = self.new_coding # 將原本的捐款者編號, 放入歷史紀錄之中
    #
    #         if self.zip is False: #使用者如果沒有填收據寄送地址郵遞區號, 則編碼前3碼為 '999'
    #             compute_code = self.env['auto.donateid'].search([('zip','=','999')])
    #             self.new_coding = '999' + str(compute_code.area_number + 1).zfill(5) # 取出當前 zip = '999' 的累積人數+1
    #             compute_code.write({
    #                 'area_number': compute_code.area_number + 1 #  寫入 zip = 'OOO' 目前的累積人數
    #             })
    #         elif self.zip and len(self.zip) < 3: # 使用者有輸入收據寄送地址的郵遞區號但不足3碼
    #             raise ValidationError(u'收據寄送地址的郵遞區號填寫錯誤，請至少填3碼的郵遞區號!')
    #         elif self.zip and len(self.zip) >= 3: # 使用者可以填3+2郵遞區號, 但是少要填3碼的郵遞區號
    #             compute_code = self.env['auto.donateid'].search([('zip', '=', self.zip[0:3])]) # 搜尋計數器裡符合使用者填入郵遞區號的資料
    #             if compute_code.zip: # 在計數器裡有找到該郵遞區號
    #                 self.new_coding = self.zip[0:3] + str(compute_code.area_number + 1).zfill(5)
    #                 compute_code.write({
    #                     'area_number': compute_code.area_number + 1 #  寫入 zip 目前的累積人數
    #                 })
    #             elif compute_code.zip is False: # 在計數器裡沒有找到該郵遞區號
    #                 self.new_coding = self.zip[0:3] + str('1').zfill(5) # 代表此捐款者為該郵遞區號捐款的第1人
    #                 self.env['auto.donateid'].create({
    #                     'zip': self.zip[0:3], # 在計數器裡創建該郵遞區號的資料
    #                     'area_number': 1 # 將累積人數設定為1
    #                 })

    @api.model
    def create(self, vals): # 建立捐款者基本資料時, 檢查郵遞區號填寫是否正確並產生捐款者編號, 這裡是覆寫odoo原本的create()
        res_id = super(NormalP, self).create(vals)
        if res_id.name is False: # 捐款者姓名欄位不得為空
            raise ValidationError(u'請輸入姓名')
        if res_id.con_phone: # 如果連絡電話有填寫, 則要檢查字串是否有非數字的字元存在, 否則不能存檔
            for ch in res_id.con_phone:
                if u'\u0030' <= ch <= u'\u0039':
                    continue
                else:
                    raise ValidationError(u'電話格式不能有非數字的字元')
        if res_id.cellphone:
            for ch in res_id.cellphone:
                if u'\u0030' <= ch <= u'\u0039':
                    continue
                else:
                    raise ValidationError(u'手機格式不能有非數字的字元')
        if res_id.zip is False: # 使用者如果沒有填收據寄送地址郵遞區號, 則無法建立此筆紀錄
            raise ValidationError(u'收據郵遞區號不能為空白')
        elif res_id.zip == True or res_id.zip_code == True: # 如果收據地址的郵遞區號或者報表地址的郵遞區號有填入

            for ch in res_id.zip:
                if not u'\u0030' <= ch <= u'\u0039': # 檢查使用者輸入的郵遞區號是否都為數字
                    raise ValidationError(u'收據郵遞區號輸入格式錯誤，請重新輸入')
                if int(res_id.zip[0]) == 0: # 郵遞區號的第一碼不得為 0
                    raise ValidationError(u'收據郵遞區號第一碼，請重新輸入')

            for ch in res_id.zip_code:
                if not u'\u0030' <= ch <= u'\u0039': # 檢查使用者輸入的郵遞區號是否都為數字
                    raise ValidationError(u'報表郵遞區號輸入格式錯誤，請重新輸入')
                if int(res_id.zip_code[0]) == 0: # 郵遞區號的第一碼不得為 0
                    raise ValidationError(u'報表郵遞區號輸入格式錯誤，請重新輸入')

        elif (res_id.zip and len(res_id.zip) < 3) or (res_id.zip_code and len(res_id.zip_code) < 3): # 使用者有輸入收據寄送地址的郵遞區號但不足3碼
            raise ValidationError(u'收據寄送地址的郵遞區號填寫錯誤，請至少填3碼的郵遞區號!')
        elif res_id.zip and len(res_id.zip) >= 3: # 使用者可以填3+2郵遞區號, 但是少要填3碼的郵遞區號
            compute_code = self.env['auto.donateid'].search([('zip', '=', res_id.zip[0:3])]) # 搜尋計數器裡符合使用者填入郵遞區號的資料
            if compute_code.zip: # 在計數器裡有找到該郵遞區號
                res_id.new_coding = res_id.zip[0:3] + str(compute_code.area_number + 1).zfill(5) # 將使用者填入的郵遞區號 + (計數器資料表該郵遞區號的統計數量+1)並補齊五位數的 0
                compute_code.write({
                    'area_number': compute_code.area_number + 1 #  寫入 zip 目前的累積人數
                })
            elif compute_code.zip is False: # 在計數器裡沒有找到該郵遞區號
                res_id.new_coding = res_id.zip[0:3] + str('1').zfill(5) # 代表此捐款者為該郵遞區號捐款的第1人
                self.env['auto.donateid'].create({
                    'zip': res_id.zip[0:3], # 在計數器裡創建該郵遞區號的資料
                    'area_number': 1 # 將累積人數設定為1
                })

        if res_id.parent.id is False: # 如果新建的捐款者資料沒有選定戶長是誰, 那麼就由系統自動將該使用者設為戶長
            res_id.write({
                'parent': res_id.id,
                'new_coding': res_id.new_coding # 給予捐款者編號
            })
        elif res_id.parent.id: # 如果有選定戶長
            old_member_code = self.env['normal.p'].search([('id','=',res_id.parent.id)]) # 搜尋該戶長的資料
            if old_member_code.w_id: # 如果該戶長有w_id, 則將捐款者的w_id 設為與戶長相同的w_id
                res_id.write({
                    'w_id': old_member_code.w_id
                })

        # data = self.env['res.users'].create({
        #     'login': res_id.new_coding,
        #     'password': "00000",
        #     'name': res_id.name,
        #     'sel_groups_15' : 15,
        # })
        # res_id.write({
        #     'donor': data.id
        # })
        return res_id

    @api.multi
    def unlink(self): # 刪除記錄前, 先檢查此筆紀錄是否有任何的捐款或者繳費紀錄, 這裡是覆寫odoo原本的unlink()
        if self.donate_history_ids.ids:
            raise ValidationError(u'該捐款者有捐款紀錄, 請勿刪除')
        if self.member_pay_history.ids:
            raise ValidationError(u'該會員有繳費紀錄, 請勿刪除')
        if self.consultant_pay_history.ids:
            raise ValidationError(u'該顧問有繳費紀錄, 請勿刪除')
        self.env['res.users'].search([('id', '=', self.donor.ids)]).unlink()
        return super(NormalP, self).unlink()