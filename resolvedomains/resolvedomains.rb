require 'resolv'
require 'set'

class Resolver
  attr_reader :ip_addresses

  def initialize(string)
    @ip_addresses = []
    if Resolver.is_ip_addr?(string)
      @ip_addresses << string
    else
      resolved = Resolver.resolve(string)
      @ip_addresses += resolved unless resolved.nil?
    end
  end

  def is_domain_here?(domain)
    ip_addresses = Resolver.resolve(domain)
    return false if ip_addresses.nil?
    ip_addresses.any? { |ip_addr| @ip_addresses.include?(ip_addr) }
  end

  def self.is_ip_addr?(string)
    !!(string =~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/)
  end

  def self.resolve(domain)
    begin
      Resolv.getaddresses(domain).map(&:to_s)
    rescue Resolv::ResolvError, Resolv::NoAnswer, Resolv::NoNameservers => e
      nil
    end
  end
end

def solve_ip_addresses(s)
  r = Resolver.new(s)
  r.ip_addresses
end

def main
  lines = $stdin.read.split("\n").uniq
  resolved = Set.new
  lines.each_slice(30) do |batch|
    batch_resolved = batch.map { |line| solve_ip_addresses(line) }.flatten.uniq
    batch_resolved.each do |ip_addr|
      unless resolved.include?(ip_addr)
        resolved << ip_addr
        puts ip_addr
      end
    end
  end
end

main
