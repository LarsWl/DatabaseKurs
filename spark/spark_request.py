from pyspark.sql.types import IntegerType
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('sport').getOrCreate()

print("Session inited")

lessons_df = spark.read.option("header", True).csv("hdfs://localhost:9000/sport_data/lessons.csv")
lessons_df = lessons_df.withColumn("price", lessons_df["price"].cast(IntegerType()))

lessons_df.groupBy("visitor_id").sum("price").show()

input("Ctrl C")
