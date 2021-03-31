sqledocs = '''
select distinct
b.DOC_HDR_ID, a.DOC_TYP_NM, a.DOC_CRTE_DT, b.CRTE_DT, a.DOC_MDFN_DT, b.ACTN_RQST_CD,
c.PRNCPL_NM, d.GRP_NM, b.QUAL_ROLE_NM,
a.FLD_NM, a.FLD_VAL
from
DSS_KR.KR_KREW_ACTN_RQST_T_v b
left join dss_kr.kr_edl_dmp_gt a on b.doc_hdr_id = a.doc_hdr_id
left join DSS_KR.KR_KRIM_PRNCPL_T_GT c on b.PRNCPL_ID = c.PRNCPL_ID
left join DSS_KR.KR_KRIM_GRP_T_GT d on b.GRP_ID = d.GRP_ID
where
a.DOC_RTE_STAT_CD = 'R'
and
b.PARNT_ID is null
and
b.ACTN_TKN_ID is null
and
a.FLD_NM in ('campus','campusTitle','concentration1','concentration2','concentrationTrack',
             'department','department1','department2','major','major1','major2','minor1','minor2')
order by b.DOC_HDR_ID, b.CRTE_DT
'''

sqlgroups = '''
Select
a.grp_nm, a.GRP_DESC, b.LAST_UPDT_DT, c.ent_id, c.frst_nm, c.MID_NM, c.lst_nm, d.PRNCPL_NM, e.PRMRY_DEPT_CD,
a.ACTV_IND groupactive, a.LAST_UPDT_DT grouplastupdate, c.DFLT_IND namedefault, c.ACTV_IND nameactive,
e.PRMRY_IND empinfoprimary, e.ACTV_IND empinfoactive, e.EMP_STAT_CD empinfostatus, e.EMP_TYP_CD empinfotype
from
dss_kr.kr_krim_grp_t_gt a,
dss_kr.kr_krim_grp_mbr_t_gt b,
dss_kr.kr_krim_ent_nm_t_gt c,
dss_kr.kr_krim_prncpl_t_gt d,
dss_kr.kr_krim_ent_emp_info_t_gt e
where
a.grp_id = b.grp_id
and
b.mbr_id = c.ent_id
and
c.ent_id = d.prncpl_id
and
c.ent_id = e.ent_id
and
a.actv_ind = 'Y' and (c.dflt_ind = 'Y' and c.actv_ind = 'Y')
and
b.actv_to_dt is null
and
(e.PRMRY_IND = 'Y' and e.actv_ind = 'Y')
and
((a.grp_nm like 'SIS.ADM.BL.%' or a.grp_nm like 'SIS.ADM.IN.%')
  --((a.grp_nm like 'SIS.ADM.BL.GRAD.%' or a.grp_nm like 'SIS.ADM.IN.GRAD.%')
     or
     (a.nmspc_cd in
       ('UGS.MAAdvDeg','UGS.COMMITTEE','UGS.CANDIDACY','UGS.PHDCOMM','UGS.PhDComm','UGS.PHDDEFENSE','UGS.STUDYABROAD','UGS.EXCEPTION'))
  );
'''