import pandas as pd
import numpy as np

# Read the data
df = pd.read_csv('labeled_netflows_with_subnet.csv')

# Convert the timestamp to a datetime object
df['ts'] = pd.to_datetime(df['ts'])

# Ensure 'ts' is the DataFrame's index
df.set_index('ts', inplace=True)

# Add small random noise to 'ts' column to ensure all timestamps are unique
df.index += pd.to_timedelta(np.random.randint(0, 1000), unit='ms')

# Calculate the number of connections an IP makes per minute in a separate DataFrame
num_connections_per_minute = df.groupby('src_ip').resample('1T')['dst_ip'].count().reset_index()
num_connections_per_minute.columns = ['src_ip', 'ts', 'num_connections_per_minute']

# Merge the new DataFrame with the original DataFrame
df = pd.merge(df.reset_index(), num_connections_per_minute, on=['src_ip', 'ts'], how='left')

# Fill NaN values with 0
df['num_connections_per_minute'].fillna(0, inplace=True)

# Ensure 'ts' is the DataFrame's index again
df.set_index('ts', inplace=True)

# Continue with the rest of your code...

# Calculate the number of unique servers an IP connects to
df['num_unique_servers'] = df.groupby('src_ip')['dst_ip'].transform('nunique')

# Calculate the total bytes transferred by an IP
df['total_bytes_transferred'] = df.groupby('src_ip')['bts'].transform('sum')

# Calculate the average number of packets exchanged per session for each pair of source and destination IPs
df['avg_packets_per_session'] = df.groupby(['src_ip', 'dst_ip'])['cnt'].transform('mean')

# Reset the index
df.reset_index(inplace=True)

# Calculate the number of SYN flags sent by an IP
df['num_syn_flags'] = df[df['flgs'].str.contains('S')].groupby('src_ip')['flgs'].transform('count')

# Calculate the number of ACK flags sent by an IP
df['num_ack_flags'] = df[df['flgs'].str.contains('A')].groupby('src_ip')['flgs'].transform('count')

# Calculate the number of RST flags sent by an IP
df['num_rst_flags'] = df[df['flgs'].str.contains('R')].groupby('src_ip')['flgs'].transform('count')

# Calculate the number of FIN flags sent by an IP
df['num_fin_flags'] = df[df['flgs'].str.contains('F')].groupby('src_ip')['flgs'].transform('count')

# Calculate the number of connections an IP makes to the same server
df['num_connections_to_same_server'] = df.groupby(['src_ip', 'dst_ip']).transform('size')

# Calculate the number of connections an IP makes to different subnets
df['num_connections_to_diff_subnets'] = df.groupby('src_ip')['dst_subnet'].transform('nunique')

# Calculate the number of connections an IP makes after network admins have gone home for the day
df['num_connections_after_hours'] = df[df['ts'].dt.hour.isin(range(18, 24))].groupby('src_ip')['dst_ip'].transform('count')

# Fill NaN values with 0
df.fillna(0, inplace=True)

# Set 'ts' as the index again
df.set_index('ts', inplace=True)

# Save the DataFrame with the new features
df.to_csv('netflows_with_features.csv', index=False)