---
name: cve
description: 根据CVE编号查找并输出对应的漏洞POC详情，包含漏洞原理、利用步骤、PoC请求/代码、检测条件和修复建议。用法：/cve CVE-2023-6018
allowed-tools: Read
---

# CVE 漏洞利用技能

## 用法

```
/cve <CVE编号>
```

支持格式：`CVE-2023-6018` / `cve-2023-6018` / `2023-6018`

## 执行步骤

1. **标准化输入**：将用户输入转换为 `CVE-YYYY-NNNNN` 格式
2. **查找索引**：在下方「CVE索引」中找到匹配行，获取文件路径（第三列）
3. **读取文件**：用 Read 工具读取该路径的文件（路径相对于本SKILL.md所在目录，即 `~/.claude/skills/cve/`）
4. **输出内容**：结构化输出以下内容：
   - CVE编号 / CVSS评分 / 漏洞类型
   - 漏洞原理
   - 验证方法
   - 利用步骤与完整PoC
   - 变量说明
   - 检测条件（如何判断利用成功）
   - 修复建议

**未找到时**：告知用户该CVE不在库中，并列出库中所有可用CVE。

---

## CVE索引（共147条）

格式：`CVE编号 | 产品 | 文件路径`

- CVE-2013-0288 | nss-pam-ldapd | data/nss_pam_ldapd/cve_2013_0288.md
- CVE-2014-0160 | OpenSSL | data/openssl/cve_2014_0160.md
- CVE-2015-1427 | ElasticSearch | data/elasticsearch/cve_2015_1427.md
- CVE-2015-3306 | ProFTPd | data/proftpd/cve_2015_3306.md
- CVE-2015-8562 | Joomla | data/joomla/cve_2015_8562.md
- CVE-2016-10033 | PHPMailer | data/phpmailer/cve_2016_10033.md
- CVE-2016-10045 | PHPMailer | data/phpmailer/cve_2016_10045.md
- CVE-2016-3088 | Apache ActiveMQ | data/apache_activemq/cve_2016_3088.md
- CVE-2016-5734 | phpMyAdmin | data/phpmyadmin/cve_2016_5734.md
- CVE-2017-12636 | Apache CouchDB | data/apache_couchdb/cve_2017_12636.md
- CVE-2017-16082 | pg_node_module | data/pg_node_module/cve_2017_16082.md
- CVE-2017-17562 | Embedthis GoAhead | data/embedthis_goahead/cve_2017_17562.md
- CVE-2017-7494 | Samba | data/samba/cve_2017_7494.md
- CVE-2018-1271 | Spring Framework | data/spring_framework/cve_2018_1271.md
- CVE-2018-1297 | Apache JMeter | data/apache_jmeter/cve_2018_1297.md
- CVE-2018-20062 | ThinkPHP | data/thinkphp/cve_2018_20062.md
- CVE-2018-7600 | Drupal | data/drupal/cve_2018_7600.md
- CVE-2019-11043 | PHP | data/php/cve_2019_11043.md
- CVE-2019-16113 | Bludit | data/bludit/cve_2019_16113.md
- CVE-2019-17564 | Apache Dubbo | data/apache_dubbo/cve_2019_17564.md
- CVE-2019-20372 | nginx | data/nginx/cve_2019_20372.md
- CVE-2020-11022 | jQuery | data/jquery/cve_2020_11022.md
- CVE-2020-11023 | jQuery | data/jquery/cve_2020_11023.md
- CVE-2020-35476 | OpenTSDB | data/opentsdb/cve_2020_35476.md
- CVE-2020-7247 | OpenSMTPD | data/opensmtpd/cve_2020_7247.md
- CVE-2021-23358 | underscore | data/underscore/cve_2021_23358.md
- CVE-2021-25646 | Apache Druid | data/apache_druid/cve_2021_25646.md
- CVE-2021-3156 | sudo | data/sudo/cve_2021_3156.md
- CVE-2021-3603 | PHPMailer | data/phpmailer/cve_2021_3603.md
- CVE-2021-41773 | Apache HTTP Server | data/apache_http_server/cve_2021_41773.md
- CVE-2021-42013 | Apache HTTP Server | data/apache_http_server/cve_2021_42013.md
- CVE-2021-43798 | Grafana | data/grafana/cve_2021_43798.md
- CVE-2021-44228 | Apache Log4j2 | data/apache_log4j2/cve_2021_44228.md
- CVE-2022-0543 | Redis | data/redis/cve_2022_0543.md
- CVE-2022-22947 | Spring Cloud Gateway | data/spring_cloud_gateway/cve_2022_22947.md
- CVE-2022-22963 | Spring Cloud Function | data/spring_cloud_function/cve_2022_22963.md
- CVE-2022-22965 | Spring Framework | data/spring_framework/cve_2022_22965.md
- CVE-2022-24706 | Apache CouchDB | data/apache_couchdb/cve_2022_24706.md
- CVE-2022-24816 | GeoServer | data/geoserver/cve_2022_24816.md
- CVE-2022-28512 | Sourcecodester Fantastic Blog CMS | data/sourcecodester_fantastic_blog_cms/cve_2022_28512.md
- CVE-2022-28524 | ED01-CMS | data/ed01_cms/cve_2022_28524.md
- CVE-2022-28525 | ED01-CMS | data/ed01_cms/cve_2022_28525.md
- CVE-2022-2900 | parse-url | data/parse_url/cve_2022_2900.md
- CVE-2022-30887 | Pharmacy Management System | data/pharmacy_management_system/cve_2022_30887.md
- CVE-2022-32991 | Web Based Quiz System | data/web_based_quiz_system/cve_2022_32991.md
- CVE-2022-41678 | Apache ActiveMQ | data/apache_activemq/cve_2022_41678.md
- CVE-2022-4223 | pgAdmin | data/pgadmin/cve_2022_4223.md
- CVE-2023-2251 | eemeli/yaml | data/eemeli_yaml/cve_2023_2251.md
- CVE-2023-23752 | Joomla | data/joomla/cve_2023_23752.md
- CVE-2023-25826 | OpenTSDB | data/opentsdb/cve_2023_25826.md
- CVE-2023-37999 | HasThemes HT Mega | data/hasthemes_ht_mega/cve_2023_37999.md
- CVE-2023-39361 | Cacti | data/cacti/cve_2023_39361.md
- CVE-2023-39662 | llama_index | data/llama_index/cve_2023_39662.md
- CVE-2023-46219 | curl | data/curl/cve_2023_46219.md
- CVE-2023-5002 | pgAdmin | data/pgadmin/cve_2023_5002.md
- CVE-2023-50564 | Pluck CMS | data/pluck_cms/cve_2023_50564.md
- CVE-2023-51449 | gradio | data/gradio/cve_2023_51449.md
- CVE-2023-51467 | Apache OFBiz | data/apache_ofbiz/cve_2023_51467.md
- CVE-2023-51483 | WP Frontend Profile | data/wp_frontend_profile/cve_2023_51483.md
- CVE-2023-6018 | mlflow/mlflow | data/mlflow_mlflow/cve_2023_6018.md
- CVE-2023-7130 | code-projects College Notes Gallery | data/code_projects_college_notes_gallery/cve_2023_7130.md
- CVE-2024-0520 | mlflow/mlflow | data/mlflow_mlflow/cve_2024_0520.md
- CVE-2024-10361 | danny-avila/librechat | data/librechat/cve_2024_10361.md
- CVE-2024-10366 | danny-avila/librechat | data/librechat/cve_2024_10366.md
- CVE-2024-11041 | vllm-project/vllm | data/vllm_project_vllm/cve_2024_11041.md
- CVE-2024-11042 | invoke-ai/invokeai | data/invoke_ai_invokeai/cve_2024_11042.md
- CVE-2024-11170 | danny-avila/librechat | data/librechat/cve_2024_11170.md
- CVE-2024-11172 | danny-avila/librechat | data/librechat/cve_2024_11172.md
- CVE-2024-12029 | invoke-ai/invokeai | data/invoke_ai_invokeai/cve_2024_12029.md
- CVE-2024-12216 | dmlc/gluon-cv | data/dmlc_gluon_cv/cve_2024_12216.md
- CVE-2024-12389 | binary-husky/gpt_academic | data/binary_husky_gpt_academic/cve_2024_12389.md
- CVE-2024-12580 | danny-avila/librechat | data/librechat/cve_2024_12580.md
- CVE-2024-1455 | langchain-ai/langchain | data/langchain_ai_langchain/cve_2024_1455.md
- CVE-2024-1558 | mlflow/mlflow | data/mlflow_mlflow/cve_2024_1558.md
- CVE-2024-1561 | gradio | data/gradio/cve_2024_1561.md
- CVE-2024-1625 | lunary-ai/lunary | data/lunary_ai_lunary/cve_2024_1625.md
- CVE-2024-1643 | lunary-ai/lunary | data/lunary_ai_lunary/cve_2024_1643.md
- CVE-2024-1739 | lunary-ai/lunary | data/lunary_ai_lunary/cve_2024_1739.md
- CVE-2024-21896 | NodeJS Node | data/nodejs_node/cve_2024_21896.md
- CVE-2024-22120 | Zabbix | data/zabbix/cve_2024_22120.md
- CVE-2024-22476 | Intel Neural Compressor | data/intel_neural_compressor/cve_2024_22476.md
- CVE-2024-2359 | lollms_web_ui | data/lollms_web_ui/cve_2024_2359.md
- CVE-2024-23897 | Jenkins | data/jenkins/cve_2024_23897.md
- CVE-2024-24762 | python-multipart | data/python_multipart/cve_2024_24762.md
- CVE-2024-25641 | Cacti | data/cacti/cve_2024_25641.md
- CVE-2024-2624 | lollms_web_ui | data/lollms_web_ui/cve_2024_2624.md
- CVE-2024-27348 | Apache HugeGraph-Server | data/apache_hugegraph_server/cve_2024_27348.md
- CVE-2024-2771 | Fluent Forms Contact Form | data/fluentforms_contact_form/cve_2024_2771.md
- CVE-2024-2912 | bentoml | data/bentoml/cve_2024_2912.md
- CVE-2024-30260 | undici | data/undici/cve_2024_30260.md
- CVE-2024-30542 | Wholesale WholesaleX | data/wholesale_wholesalex/cve_2024_30542.md
- CVE-2024-3098 | llama_index | data/llama_index/cve_2024_3098.md
- CVE-2024-31459 | Cacti | data/cacti/cve_2024_31459.md
- CVE-2024-31611 | SeaCMS | data/seacms/cve_2024_31611.md
- CVE-2024-32167 | online_medicine_ordering_system | data/online_medicine_ordering_system/cve_2024_32167.md
- CVE-2024-3234 | gaizhenbiao/chuanhuchatgpt | data/gaizhenbiao_chuanhuchatgpt/cve_2024_3234.md
- CVE-2024-32511 | Astoundify Simple Registration for WooCommerce | data/astoundify_simple_registration/cve_2024_32511.md
- CVE-2024-32964 | Lobe Chat | data/lobe_chat/cve_2024_32964.md
- CVE-2024-32980 | Spin | data/spin/cve_2024_32980.md
- CVE-2024-32986 | PWAsForFirefox | data/pwasforfirefox/cve_2024_32986.md
- CVE-2024-34070 | Froxlor | data/froxlor/cve_2024_34070.md
- CVE-2024-3408 | man-group/dtale | data/man_group_dtale/cve_2024_3408.md
- CVE-2024-34340 | Cacti | data/cacti/cve_2024_34340.md
- CVE-2024-34359 | llama-cpp-python | data/llama_cpp_python/cve_2024_34359.md
- CVE-2024-34716 | PrestaShop | data/prestashop/cve_2024_34716.md
- CVE-2024-3495 | Country State City Dropdown CF7 plugin for WordPress | data/country_state_city_dropdown_cf7_plugin_for_wordpress/cve_2024_3495.md
- CVE-2024-35187 | Stalwart Mail Server | data/stalwart_mail_server/cve_2024_35187.md
- CVE-2024-3552 | Web Directory Free WordPress plugin | data/web_directory_free_wordpress_plugin/cve_2024_3552.md
- CVE-2024-36401 | GeoServer | data/geoserver/cve_2024_36401.md
- CVE-2024-36412 | SuiteCRM | data/suitecrm/cve_2024_36412.md
- CVE-2024-36675 | LyLme_spage | data/lylme_spage/cve_2024_36675.md
- CVE-2024-36779 | Stock Management System | data/stock_management_system/cve_2024_36779.md
- CVE-2024-36858 | Jan | data/jan/cve_2024_36858.md
- CVE-2024-37388 | ebookmeta | data/ebookmeta/cve_2024_37388.md
- CVE-2024-37831 | itsourcecode Payroll Management System | data/itsourcecode_payroll_management_system/cve_2024_37831.md
- CVE-2024-37849 | itsourcecode Billing System | data/itsourcecode_billing_system/cve_2024_37849.md
- CVE-2024-39907 | 1Panel | data/1panel/cve_2024_39907.md
- CVE-2024-41990 | Django | data/django/cve_2024_41990.md
- CVE-2024-4223 | Tutor LMS | data/tutor_lms/cve_2024_4223.md
- CVE-2024-4320 | lollms_web_ui | data/lollms_web_ui/cve_2024_4320.md
- CVE-2024-4323 | Fluent Bit | data/fluent_bit/cve_2024_4323.md
- CVE-2024-4442 | Salon booking system | data/salon_booking_system/cve_2024_4442.md
- CVE-2024-4443 | Business Directory Plugin – Easy Listing Directories for WordPress | data/business_directory_plugin/cve_2024_4443.md
- CVE-2024-4701 | Genie | data/genie/cve_2024_4701.md
- CVE-2024-4940 | gradio | data/gradio/cve_2024_4940.md
- CVE-2024-4941 | gradio | data/gradio/cve_2024_4941.md
- CVE-2024-4956 | Sonatype Nexus Repository Manager | data/sonatype_nexus/cve_2024_4956.md
- CVE-2024-5084 | Hash Form – Drag & Drop Form Builder for WordPress | data/hash_form_wordpress/cve_2024_5084.md
- CVE-2024-5206 | scikit-learn | data/scikit_learn/cve_2024_5206.md
- CVE-2024-5314 | Dolibarr ERP/CRM | data/dolibarr_erp_crm/cve_2024_5314.md
- CVE-2024-5315 | Dolibarr ERP/CRM | data/dolibarr_erp_crm/cve_2024_5315.md
- CVE-2024-5452 | lightning-ai/pytorch-lightning | data/lightning_ai_pytorch_lightning/cve_2024_5452.md
- CVE-2024-5569 | jaraco/zipp | data/jaraco_zipp/cve_2024_5569.md
- CVE-2024-5998 | langchain-ai/langchain | data/langchain_ai_langchain/cve_2024_5998.md
- CVE-2024-6345 | pypa/setuptools | data/pypa_setuptools/cve_2024_6345.md
- CVE-2024-6827 | gunicorn | data/gunicorn/cve_2024_6827.md
- CVE-2024-7983 | open-webui | data/open_webui/cve_2024_7983.md
- CVE-2024-8020 | lightning-ai/pytorch-lightning | data/lightning_ai_pytorch_lightning/cve_2024_8020.md
- CVE-2024-8438 | modelscope/agentscope | data/modelscope_agentscope/cve_2024_8438.md
- CVE-2024-8954 | composiohq/composio | data/composiohq_composio/cve_2024_8954.md
- CVE-2024-9070 | bentoml | data/bentoml/cve_2024_9070.md
- CVE-2024-9701 | kedro-org kedro-org/kedro | data/kedro_org_kedro/cve_2024_9701.md
- CVE-2025-0453 | mlflow/mlflow | data/mlflow_mlflow/cve_2025_0453.md
- CVE-2025-32433 | Erlang/OTP | data/erlang_otp/cve_2025_32433.md
- CVE-2025-3248 | Langflow AI | data/langflow_ai/cve_2025_3248.md
- CVE-2025-55182 | react | data/react/cve_2025_55182.md
- CVE-2025-67303 | ComfyUI-Manager | data/comfyui_manager/cve_2025_67303.md
