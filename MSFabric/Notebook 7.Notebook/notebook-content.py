# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
%pip install "https://raw.githubusercontent.com/m-kovalsky/fabric_cat_tools/main/fabric_cat_tools-0.4.1-py3-none-any.whl"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import fabric_cat_tools as fct
from fabric_cat_tools.TOM import connect_semantic_model


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import fabric_cat_tools as fct
fct.clear_cache(
        dataset='CMS Medicare Part D Star Schema Template ',
        #workspace=" "
)




# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

fct.clone_report(
            report = 'CMS Medicare Part D Star Schema Template ',
            cloned_report = 'CMS Medicare Part D Star Schema Templatefct',
            #workspace = None,
            #target_workspace = None,
            #target_dataset = None
            )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
